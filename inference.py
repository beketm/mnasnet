from torchvision import models, transforms
import torch.nn as nn
import torch
from PIL import Image
from io import BytesIO
import base64


PATH = "mnasnet_weights.pt"
device = "cpu"
class_names=['akorda', 'baiterek', 'khanshatyr', 'mangilikel', 'mosque', 'nuralem', 'piramida', 'shabyt']
num_classes = len(class_names)

class Inference:
    
    def __init__(self,):
        self.model = self.get_model()

    def get_model(self):
        model_ft = models.mnasnet1_3() 

        # Freeze all the required layers (i.e except last conv block and fc layers)
        for params in model_ft.parameters():
            params.requires_grad = False

        # Modify fc layers to match num_classes
        num_ftrs=model_ft.classifier[-1].in_features
        model_ft.classifier=nn.Sequential(
            nn.Dropout(0.2, inplace=True),
            nn.Linear(num_ftrs, num_classes, bias=True)
        )
        model_ft = model_ft.to(device)
        model_ft.load_state_dict(torch.load(PATH, map_location=torch.device('cpu')))
        model_ft.eval()
        return model_ft


    def transform_image(self, image):
        my_transforms = transforms.Compose([
                                    transforms.Resize(size=256),
                                    transforms.CenterCrop(size=224),
                                    transforms.ToTensor(),
                                    transforms.Normalize([0.485, 0.456, 0.406],            
                                                        [0.229, 0.224, 0.225])])

        return my_transforms(image).unsqueeze(0)

    def get_prediction(self, image):
        tensor = self.transform_image(image)
        # print(tensor.shape)
        tensor = tensor.to(device)
        output = self.model(tensor)
        print(output)
        probs = torch.nn.functional.softmax(output, dim=1)
        conf, classes = torch.max(probs, 1)
        return conf.item(), class_names[classes.item()]


    def read_imagefile(self, file) -> Image.Image:
        # image = Image.open(BytesIO(file)).convert('RGB')
        # image = Image.open(file).convert('RGB')
        image = Image.open(BytesIO(base64.b64decode(file))).convert('RGB')
        return image
    
    def classify_image(self, file):
        # extension = file.name.split(".")[-1] in ("jpg", "jpeg", "png")
        # if not extension:
        #     return "Image must be jpg or png format!"
        image = self.read_imagefile(file)

        prediction = self.get_prediction(image)
        response = {"probability" : prediction[0], "class":prediction[1]}
        return response

if __name__=="__main__":
    infer = Inference()
    with open("r.png", "rb") as image_file:
        print(infer.classify_image(image_file))

    # obj = base64.b64decode(encoded_string)
    # print(type(obj))
    # print(infer.classify_image(obj))
