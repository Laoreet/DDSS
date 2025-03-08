import torch.nn as nn
import torchvision.models as models
import torch.nn.functional as F
import torch
import matplotlib.pyplot as plt
import io
from PIL import Image
import base64

class MedicalNet(nn.Module):
    def __init__(self):
        super(MedicalNet, self).__init__()
        
        self.model = models.video.r3d_18(models.video.R3D_18_Weights.KINETICS400_V1)
        # Изменение количества входных каналов в первом сверточном слое
        self.model.stem[0] = nn.Conv3d(3, 64, kernel_size=(3, 7, 7), stride=(1, 2, 2), padding=(1, 3, 3), bias=False)
        self.model.fc = nn.Linear(self.model.fc.in_features, 1)

    def forward(self, x):
        return self.model(x)
    
class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.activations = None
        self.gradients = None

        # Регистрируем хуки для захвата активаций и градиентов
        target_layer.register_forward_hook(self.save_activations)
        target_layer.register_backward_hook(self.save_gradients)

    def save_activations(self, module, input, output):
        self.activations = output

    def save_gradients(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def forward(self, x):
        return self.model(x)

    def backward(self, output):
        self.model.zero_grad()
        output.backward(torch.ones_like(output), retain_graph=True)

    def generate(self, x, class_idx=None):
        # Forward pass
        output = self.forward(x)

        # Если класс не указан, используем максимальный класс
        if class_idx is None:
            class_idx = torch.argmax(output, dim=1)

        # Backward pass
        self.backward(output[:, class_idx])

        # Вычисляем веса
        weights = torch.mean(self.gradients, dim=(2, 3, 4), keepdim=True)

        # Создаем карту внимания
        cam = torch.sum(self.activations * weights, dim=1, keepdim=True)
        cam = F.relu(cam)  # Применяем ReLU

        # Интерполируем карту до размеров входного изображения
        cam = F.interpolate(cam, size=x.shape[2:], mode='trilinear', align_corners=False)

        # Нормализуем карту
        cam = (cam - cam.min()) / (cam.max() - cam.min())

        return cam
    
def get_attention_map_base64(model, input_ct):
    target_layer = model.model.layer4[1].conv2
    grad_cam = GradCAM(model, target_layer)
    slice_idx = 77

    cam = grad_cam.generate(input_ct)
    fig, ax = plt.subplots()

    # Отображение исходного изображения
    ax.imshow(input_ct[0, 2, slice_idx].cpu(), cmap='bone')

    # Наложение карты внимания
    ax.imshow(cam[0, 0, slice_idx].detach().cpu().numpy(), cmap='afmhot', alpha=0.5)

    # Удаление осей
    ax.axis('off')

    # Сохранение фигуры в буфер
    buf = io.BytesIO()
    plt.savefig(buf, format='PNG', bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    # Чтение изображения из буфера
    buf.seek(0)
    img = Image.open(buf)

    # Кодирование изображения в base64
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

    return img_str

