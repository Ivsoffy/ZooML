from efficientnet_pytorch import EfficientNet
# from resnet_pytorch import ResNet
from torchvision.models import resnet50, ResNet50_Weights


def get_efficientnet_model(num_classes: int = 18):
    model = EfficientNet.from_pretrained('efficientnet-b0', num_classes=num_classes)
    return model

def get_resnet_model(num_classes: int = 18):
    # model = ResNet.from_pretrained("resnet18", num_classes=num_classes)
    model = resnet50(weights=ResNet50_Weights.DEFAULT)
    return model