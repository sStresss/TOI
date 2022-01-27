from rest_framework import serializers
from .models import Cabinets, Modules, ColorPixel


class CabinetSerializer(serializers.ModelSerializer):
    # modules = serializers.SlugRelatedField(many=True, read_only=True, slug_field='red_module')
    # modules = serializers.StringRelatedField(many=True, read_only=True)

    modules = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # test_module = serializers.StringRelatedField(many=True)

    class Meta:
        model = Cabinets
        fields = "__all__"


class ColorPixelSerializer(serializers.ModelSerializer):

    class Meta:
        model = ColorPixel
        fields = ['red_module', 'green_module', 'blue_module', 'module']


class ModuleSerializer(serializers.ModelSerializer):
    # cabinet = serializers.StringRelatedField(many=True, read_only=True)
    # test_module = serializers.StringRelatedField(many=True)
    color_pixel = ColorPixelSerializer(many=True)
    # color_pixel = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Modules
        fields = ['item_module', 'module_broken', 'cabinet', 'color_pixel']
        # , 'red_module', 'green_module', 'blue_module'


class CabinetDepthSerializer(serializers.ModelSerializer):
    # modules = serializers.StringRelatedField(many=True, read_only=True)
    # modules = serializers.SlugRelatedField(many=True, read_only=True, slug_field='red_module')
    modules = ModuleSerializer(many=True)

    # modules = serializers.SlugRelatedField(many=True, read_only=True, slug_field='red_module')

    class Meta:
        model = Cabinets
        # fields = "__all__"
        fields = ['item', 'number_of_broken', 'percent_broken', 'modules']

        depth = 1


class CabinetNestedSerializer(serializers.ModelSerializer):
    # делаем наследование
    # item = CabinetSerializer(many=True)
    # skill = SkillSerializer(many=True)
    # test_module = serializers.StringRelatedField(many=True)
    # уточняем поле
    # module = serializers.CharField(source="get_modules_display", read_only=True)

    class Meta:
        model = Cabinets
        fields = "__all__"
