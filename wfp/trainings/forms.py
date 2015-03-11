from django.forms import ModelForm

from models import Training


class TrainingForm(ModelForm):
    """
    Form to add/update a training
    """

    class Meta:
        model = Training
