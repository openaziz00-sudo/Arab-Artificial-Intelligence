# دليل API وحزمة `arab-prompts`

يوفّر المشروع طبقتين للاستخدام: حزمة Python خفيفة للوصول البرمجي إلى الكتالوج، وخادم FastAPI لتكاملات الويب والتطبيقات.

## التثبيت

للاستخدام البرمجي الأساسي:

```bash
python -m pip install arab-prompts
```

من نسخة المستودع المحلية:

```bash
python -m pip install .
```

لتشغيل API والبحث الدلالي:

```bash
python -m pip install -r requirements-api.txt
```

## استخدام الحزمة

```python
from arab_prompts import categories, get_prompt, prompts, search

all_prompts = prompts()
print(len(all_prompts))  # 1650
print(categories()["code"])

prompt = get_prompt(1)
print(prompt["title"] if prompt else "غير موجود")

results = search("خطة محتوى أسبوعية", category="marketing", limit=5)
for item in results:
    print(item["id"], item["title"])
```

`search()` في الحزمة يستخدم بحثًا نصيًا سريعًا ولا يحتاج إلى اعتماديات خارجية.

## تشغيل الخادم

```bash
uvicorn api.main:app --reload
```

- التوثيق التفاعلي: <http://localhost:8000/docs>
- مخطط OpenAPI: <http://localhost:8000/openapi.json>

## نقاط النهاية

### `GET /prompts`

إرجاع صفحة من الكتالوج.

```bash
curl 'http://localhost:8000/prompts?category=code&limit=10&offset=0'
```

المعاملات: `category` اختياري، `limit` من 1 إلى 200، و`offset` يبدأ من صفر.

### `GET /prompts/{id}`

إرجاع سجل واحد بالمعرّف الرقمي، أو `404` إذا لم يوجد.

```bash
curl http://localhost:8000/prompts/1
```

### `GET /categories`

إرجاع مفاتيح الفئات وأسمائها العربية وعدد السجلات في كل فئة.

### `GET /search`

البحث في الكتالوج نصيًا أو دلاليًا.

```bash
curl 'http://localhost:8000/search?q=أريد%20كتابة%20خطة%20تسويق&semantic=true&limit=10'
```

- `q`: الاستعلام المطلوب، وهو إلزامي.
- `semantic`: مفعّل افتراضيًا. عند عدم توفر `sentence-transformers` يعود الخادم تلقائيًا إلى البحث النصي.
- `category`: تصفية اختيارية.
- `limit`: من 1 إلى 100.

يُحمّل النموذج المحلي عند أول طلب دلالي. يمكن تخصيصه عبر:

```bash
export ARAB_PROMPTS_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

### `GET /health`

فحص سريع لحالة الخدمة وعدد السجلات والفئات.

## ملاحظات الإنتاج

- ضع API خلف reverse proxy مع HTTPS عند نشره للعامة.
- أضف تحديد معدل الطلبات ومصادقة إذا كان الاستخدام خاصًا أو كثيفًا.
- نموذج embeddings قد يحتاج ذاكرة ومساحة أكبر عند أول تشغيل؛ يمكن استخدام `semantic=false` في البيئات الخفيفة.
- CORS مفتوح للقراءة العامة في النسخة الحالية لتسهيل ربط الواجهة الثابتة. قيّده إلى نطاقك عند إضافة بيانات خاصة.
