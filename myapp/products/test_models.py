from rest_framework.test import APITestCase
from .models import Product, Ingredient


class IngredientModelTest(APITestCase):

    """ all tests related with Ingredient Model """

    @classmethod
    def setUpTestData(cls):
        Ingredient.objects.create(
            id=1, name="test-ingredient", oily="O", dry="", sensitive="X"
        )

    def test_name_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field("name").max_length
        self.assertEquals(max_length, 100)

    def test_oily_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field("oily").max_length
        self.assertEquals(max_length, 1)

    def test_dry_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field("dry").max_length
        self.assertEquals(max_length, 1)

    def test_sensitive_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field("sensitive").max_length
        self.assertEquals(max_length, 1)


class ProductModelTest(APITestCase):

    """ all tests related with Product Model """

    @classmethod
    def setUpTestData(cls):

        Ingredient.objects.create(
            id=2, name="ingredient1", oily="O", dry="", sensitive="X"
        )
        Ingredient.objects.create(
            id=3, name="ingredient2", oily="O", dry="X", sensitive=""
        )
        Ingredient.objects.create(
            id=4, name="ingredient3", oily="X", dry="", sensitive="O"
        )
        instance = Product.objects.create(
            id=1,
            imageId="test_image_id",
            name="test_image_name",
            price=10000,
            gender="male",
            category="Skin care",
            monthlySales=1000,
        )
        ingredients = Ingredient.objects.all()
        instance.ingredients.set(ingredients)

    def test_imageId_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field("imageId").max_length
        self.assertEquals(max_length, 100)

    def test_name_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field("name").max_length
        self.assertEquals(max_length, 100)

    def test_gender_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field("gender").max_length
        self.assertEquals(max_length, 6)

    def test_category_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field("category").max_length
        self.assertEquals(max_length, 11)

    def test_category_default(self):
        product = Product.objects.get(id=1)
        default = product._meta.get_field("category").default
        self.assertEquals(default, "skincare")

    def test_category_choices(self):
        CATEGORY_CHOICES = (
            ("skincare", "Skin care"),
            ("maskpack", "Mask pack"),
            ("suncare", "Sun care"),
            ("basemakeup", "Base makeup"),
        )
        product = Product.objects.get(id=1)
        choices = product._meta.get_field("category").choices
        self.assertEquals(choices, CATEGORY_CHOICES)

    def test_imgUrl(self):
        product = Product.objects.get(id=1)
        self.assertEquals(product.imgUrl()[-4:], ".jpg")

    def test_ingredient_str(self):
        product = Product.objects.get(id=1)
        self.assertEquals(
            product.ingredient_str(), "ingredient1,ingredient2,ingredient3"
        )

    def test_convert_char_to_score(self):
        product = Product.objects.get(id=1)
        ingredient1 = product.ingredients.all()[0]
        oily_score = product.convert_char_to_score(ingredient1.oily)
        dry_score = product.convert_char_to_score(ingredient1.dry)
        sensitive_score = product.convert_char_to_score(ingredient1.sensitive)
        self.assertEquals([1, 0, -1], [oily_score, dry_score, sensitive_score])

    def test_calculate_score(self):
        skin_type = "oily"
        product = Product.objects.get(id=1)
        score = product.calculate_score(skin_type)
        self.assertEquals(score, 1)
