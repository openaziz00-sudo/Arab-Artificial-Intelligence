# ai العرب — مكتبة البرومبتات العربية

**مكتبة عربية مفتوحة تضم ١٬٦٥٠ برومبتًا موزعة على ١٧ فئة.** صُممت للمطورين وصنّاع المحتوى والطلاب والباحثين الذين يريدون نقطة بداية عربية قابلة للبحث والنسخ بدل كتابة كل توجيه من الصفر. اختر قالبًا، أضف سياقك، ثم راجع الناتج قبل استخدامه.

## ابدأ خلال ٣٠ ثانية

يتطلب المشروع Python 3 ومتصفحًا حديثًا:

```bash
git clone https://github.com/openaziz00-sudo/Arab-Artificial-Intelligence.git
cd Arab-Artificial-Intelligence
python3 -m http.server 8000
```

افتح [http://localhost:8000](http://localhost:8000). ابحث أو اختر فئة، ثم انسخ البرومبت وعدّله ليناسب مهمتك.

## ما الذي يقدمه؟

- بحث في أسماء المهام والأوصاف ونصوص البرومبتات.
- تصفية حسب ١٧ فئة، مع عرض أعداد العناصر بكل فئة.
- نسخ البرومبتات وتنزيل نتائج البحث كملف JSON.
- واجهة عربية RTL متجاوبة، ووضع داكن، ومفضلة محفوظة محليًا.
- ملف بيانات مستقل `prompts.json` يمكن استخدامه أو دمجه في تطبيقات أخرى.
- API بسيط بـ FastAPI مع `/prompts` و`/prompts/{id}` و`/search?q=...` و`/categories`.
- بحث دلالي محلي اختياري عبر `sentence-transformers`، مع رجوع تلقائي إلى بحث نصّي خفيف.
- حزمة Python قابلة للتثبيت باسم `arab-prompts` للاستيراد داخل مشاريعك.
- سير عمل GitHub Actions ينشر الواجهة الثابتة تلقائيًا إلى GitHub Pages.

## API والبحث الدلالي

ثبّت اعتماديات الـ API والبحث الدلالي ثم شغّل الخادم:

```bash
python3 -m pip install -r requirements-api.txt
uvicorn api.main:app --reload
```

بعدها افتح `http://localhost:8000/docs`. أمثلة:

```bash
curl 'http://localhost:8000/categories'
curl 'http://localhost:8000/prompts?category=code&limit=10'
curl 'http://localhost:8000/search?q=كيف أكتب خطة تسويقية&semantic=true'
```

يُحمّل نموذج `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` محليًا عند أول بحث دلالي، ولا تُرسل بيانات البحث إلى خدمة خارجية. يمكن تغيير النموذج عبر المتغير `ARAB_PROMPTS_MODEL`. وإذا لم تكن اعتماديات embeddings مثبتة، يعمل `/search` تلقائيًا بالبحث النصّي.

## حزمة Python

```bash
python3 -m pip install .
```

```python
from arab_prompts import categories, get_prompt, search

print(len(categories()))
print(get_prompt(1)["title"])
results = search("خطة محتوى")
```

## محتويات المستودع

- `index.html` — واجهة المكتبة وسلوك البحث والتصفية.
- `prompts.json` — ١٬٦٥٠ سجلًا في ١٧ فئة.
- `api/main.py` — خادم FastAPI ونقاط النهاية العامة.
- `arab_prompts/` — الحزمة القابلة للتثبيت ومحرك البحث الدلالي.
- `docs/api.md` — دليل الاستخدام البرمجي الكامل ومرجع نقاط النهاية.
- `CHANGELOG.md` — سجل التغييرات والإصدارات.
- `.github/workflows/pages.yml` — نشر GitHub Pages عند الدفع إلى `main`.
- `tests/test_catalog.py` — اختبارات سلامة JSON والسجلات والفئات وتطابق الأعداد.
- `CONTRIBUTING.md` — إرشادات المساهمة والتحقق.
- `LICENSE` — ترخيص MIT.
- `extend_catalog.py` و`import_role_prompts.py` — أدوات إضافة السجلات إلى البنية الحالية.

## الاختبار

شغّل الاختبارات من جذر المشروع بعد كل تعديل على البيانات أو الواجهة:

```bash
python3 -m unittest discover -s tests -v
```

وتعمل الاختبارات تلقائيًا عبر GitHub Actions عند كل push أو Pull Request، بينما ينشر سير العمل `pages.yml` الواجهة الثابتة على GitHub Pages. فعّل GitHub Pages من إعدادات المستودع باختيار **GitHub Actions** كمصدر النشر.

## المساهمة

المساهمات مرحب بها. اطلع على [CONTRIBUTING.md](CONTRIBUTING.md) لتنسيق السجلات، ومعايير القبول، وطريقة تشغيل الاختبارات قبل فتح طلب دمج.

## الترخيص

المشروع متاح بموجب [MIT License](LICENSE). عند تقديم مساهمة، فإنك توافق على إتاحتها بموجب الترخيص نفسه.

### ملكية البرومبتات وإعادة الاستخدام التجاري

جميع نصوص البرومبتات الأصلية في `prompts.json` وعددها ١٬٦٥٠ من تأليف وملكية صاحب المستودع، وليست مقتبسة من مجموعة بيانات خارجية. يسمح المالك بإعادة استخدامها ونسخها وتعديلها ودمجها في مشاريع شخصية وتجارية، مع الإبقاء على إشعار الملكية والإشارة إلى هذا المستودع عند توزيع نسخة كبيرة من الكتالوج أو إعادة نشره. لا تنطبق هذه الملاحظة على أي خط أو مكتبة أو مادة خارجية مذكورة في المشروع؛ تبقى تلك المواد خاضعة لتراخيصها الأصلية.

## ملاحظات المحتوى

البرومبتات قوالب قابلة للتعديل وليست نتائج مختبرة على نموذج محدد. راجع الحقائق والأرقام والإرشادات المهنية من مصادر موثوقة، ولا تُدخل أسرارًا أو بيانات شخصية في أدوات عامة. راجع الترخيص قبل إعادة استخدام أي مادة يملك طرف ثالث حقوقها.

## التواصل

- البريد: [7drabd1@gmail.com](mailto:7drabd1@gmail.com)
- المستودع: [openaziz00-sudo/Arab-Artificial-Intelligence](https://github.com/openaziz00-sudo/Arab-Artificial-Intelligence)
