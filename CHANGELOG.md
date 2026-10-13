# سجل التغييرات

تتبع هذه الصفحة التغييرات المهمة في مشروع **ai العرب**.

## [Unreleased]

- إصلاح سير عمل GitHub Actions لتثبيت `fastapi` و`httpx` قبل تشغيل اختبارات `TestClient`.

## [0.1.0] — 2026-10-13

### أضيف

- API مبني على FastAPI لنقاط `/prompts` و`/prompts/{id}` و`/search` و`/categories` و`/health`.
- بحث دلالي محلي اختياري باستخدام `sentence-transformers` مع fallback للبحث النصي.
- حزمة Python قابلة للتثبيت باسم `arab-prompts` وتضم الكتالوج داخل wheel.
- توثيق API وأمثلة استخدام في `docs/api.md`.
- اختبارات مباشرة لنقاط API باستخدام `fastapi.testclient.TestClient`.
- نشر تلقائي للواجهة الثابتة عبر GitHub Pages.
- توضيح ملكية المؤلف للبرومبتات وحقوق إعادة استخدامها تجاريًا.

### تحقق

- جميع اختبارات الكتالوج والحزمة وAPI تمر بنجاح.
- تم التحقق من بناء حزمة wheel وتضمين `prompts.json`.
