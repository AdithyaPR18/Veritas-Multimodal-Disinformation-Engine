import torch
import torch.nn as nn
from transformers import BertModel
from torchvision.models import resnet50, ResNet50_Weights

class TextEncoder(nn.Module):
    def __init__(self, pretrained=True):
        super(TextEncoder, self).__init__()
        if pretrained:
            self.bert = BertModel.from_pretrained('bert-base-uncased')
        else:
            # Useful for testing without downloading weights immediately if needed, 
            # though usually we want pretrained.
            from transformers import BertConfig
            self.bert = BertModel(BertConfig())
            
    def forward(self, input_ids, attention_mask):
        # BERT output: (last_hidden_state, pooler_output)
        # We use pooler_output for classification tasks (size 768)
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        return outputs.pooler_output

class VisionEncoder(nn.Module):
    def __init__(self, pretrained=True):
        super(VisionEncoder, self).__init__()
        weights = ResNet50_Weights.DEFAULT if pretrained else None
        resnet = resnet50(weights=weights)
        # Remove the final classification layer (fc)
        # ResNet structure: ... -> avgpool -> fc
        # We want the output of avgpool flattened.
        
        # Taking all layers except the last one (fc)
        self.backbone = nn.Sequential(*list(resnet.children())[:-1])

    def forward(self, x):
        # x shape: (batch_size, 3, 224, 224)
        features = self.backbone(x)
        # features shape: (batch_size, 2048, 1, 1)
        return torch.flatten(features, 1)

class FusionModule(nn.Module):
    def __init__(self, text_dim=768, vision_dim=2048, hidden_dim=512):
        super(FusionModule, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(text_dim + vision_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )

    def forward(self, text_features, vision_features):
        combined = torch.cat((text_features, vision_features), dim=1)
        return self.fc(combined)

class VeritasNet(nn.Module):
    def __init__(self):
        super(VeritasNet, self).__init__()
        self.text_encoder = TextEncoder()
        self.vision_encoder = VisionEncoder()
        self.fusion_module = FusionModule()

    def forward(self, input_ids, attention_mask, image):
        text_features = self.text_encoder(input_ids, attention_mask)
        vision_features = self.vision_encoder(image)
        authenticity_score = self.fusion_module(text_features, vision_features)
        return authenticity_score
