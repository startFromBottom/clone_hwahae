from drf_yasg import openapi

products_list_api_documents = """

## description

### 상품 목록 조회

피부 타입 별로 상품 목록을 필터링해 조회할 수 있습니다.

**기능 상세**

- 주어진 피부 타입에 대한 성분 점수를 계산해서 높은 상품 순으로 보여집니다. 점수가 같다면 낮은 가격의 상품을 먼저 표시합니다.

- 상품 목록을 50개 단위로 페이징 합니다. 인자로 페이지 번호가 주어지면, 해당되는 상품 목록이 보여집니다.

- 상품 카테고리를 선택할 수 있습니다.

- 제외해야 하는 성분들을 지정할 수 있습니다.
    
    - exclude_ingredient 인자로 전달한 성분들을 모두 가지지 않는 상품들만 목록에 포함합니다.

- 포함해야 하는 성분들을 지정할 수 있습니다.

- include_ingredient 인자로 전달한 성분들을 모두 가지고 있는 상품들만 목록에 포함합니다.

**Request Header 구조 예시**

    GET /products?skin_type=dry
    Content-Type: application/json


**Sample Call**

    /products?skin_type=oily&category=skincare&page=3&include_ingredient=Glycerin

**Success Response(Example)**

    [
        {
        "id": 17,
        "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
        "name": "화해 에센스 토너",
        "price": 23000,
        "ingredients": "Glycerin,Methyl Gluceth-20,Pulsatilla Koreana Extract,Purified Water",
        "monthlySales": 1682
        },
        {
        "id": 23,
        "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
        "name": "화해 엔젤 토너",
        "price": 4800,
        "ingredients": "Glycerin,Sodium Hyaluronate,Xanthan Gum,Niacinamide,Orchid Extract",
        "monthlySales": 463
        },


        ...


        {
        "id": 88,
        "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
        "name": "화해 화이트 브라이트닝 소프너 인리치드",
        "price": 24000,
        "ingredients": "Glycerin,Alcohol,Purified Water,Vinyl Dimethicone,PEG-10 Dimethicone",
        "monthlySales": 4437
        }
    ]


"""

products_list_params = [
    openapi.Parameter(
        "skin_type",
        openapi.IN_QUERY,
        description="(필수) oily/건성dry/sensitive 중 택 1",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "category",
        openapi.IN_QUERY,
        description="(선택) 상품 카테고리",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "exclude_ingredient",
        openapi.IN_QUERY,
        description="(선택) 제외해야 하는 성분 목록(콤마로 구분)",
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        "include_ingredient",
        openapi.IN_QUERY,
        description="(선택) 포함해야 하는 성분 목록(콤마로 구분)",
        type=openapi.TYPE_STRING,
    ),
]

product_detail_api_documents = """

## description

### 상품 목록 조회

상품 상세 정보를 조회할 수 있습니다. 같은 카테고리의 상위 3개 추천 상품들도 함께 조회할 수 있습니다.

**기능 상세**

- 상품 id로 특정 상품의 상세 정보를 조회할 수 있습니다.

- 이미지 id를 base URL과 조합해 상품 이미지를 불러올 수 있는 URL을 보여줍니다.

- 같은 카테고리의 상품 중 상위 3개의 추천 상품 정보를 조회할 수 있습니다.

    - 인자로 받은 피부 타입에 대한 성분 점수가 높은 순서로 추천합니다. 점수가 같다면, 가격이 낮은 상품을 먼저 추천합니다.

    - 추천 상품 정보는 상품 아이디, 상품 썸네일 이미지 URL, 상품명, 가격 을 포함합니다.


**Request Header 구조 예시**

    GET /product/17?skin_type=oily
    Content-Type: application/json

**Sample Call**

    /product/17?skin_type=oily

**Success Response(Example)**

    [
        {
        "id": 17,
        "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/image/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
        "name": "화해 에센스 토너",
        "price": 23000,
        "gender": "all",
        "category": "skincare",
        "ingredients": "Glycerin,Methyl Gluceth-20,Pulsatilla Koreana Extract,Purified Water",
        "monthlySales": 1682
        },
        {
        "id": 23,
        "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
        "name": "화해 엔젤 토너",
        "price": 33000
        },
        {
        "id": 37,
        "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
        "name": "화해 화이트 브라이트닝 소프너 인리치드",
        "price": 24800
        },
        {
        "id": 141,
        "imgUrl": "https://grepp-programmers-challenges.s3.ap-northeast-2.amazonaws.com/2020-birdview/thumbnail/00316276-7d5d-47d5-bfd0-a5181cd7b46b.jpg",
        "name": "화해 퍼펙트 스킨케어",
        "price": 14800
        }
    ]


"""

product_detail_params = [
    openapi.Parameter(
        "skin_type",
        openapi.IN_QUERY,
        description="(필수) oily/건성dry/sensitive 중 택 1",
        type=openapi.TYPE_STRING,
    ),
]
