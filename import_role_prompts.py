#!/usr/bin/env python3
"""Import Arabic {act, prompt} records into the library's existing catalog schema."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
CATALOG = ROOT / "prompts.json"


def has(text: str, *terms: str) -> bool:
    return any(term.casefold() in text.casefold() for term in terms)


def classify(act: str, prompt: str) -> str:
    text = f"{act} {prompt}"
    if has(text, "موارد بشرية", "توظيف", "تقييم أداء", "تنمية قيادات", "تطوير مهني", "علاقات عمالية", "موظف جديد", "تدريب وتطوير", "تحفيز موظفين", "تعويضات ومزايا", "تطوير مؤسسي", "ثقافة تنظيمية"):
        return "hr"
    if has(text, "مدرس", "معلم", "تعليم", "تعليمي", "مدرب", "مناهج", "تربوي", "طالب", "أستاذ", "تعلم", "دراسي", "تدريس", "مستشار تعليمي", "مدرسة", "جامعة", "تدريب مهني"):
        return "learning"
    if has(text, "seo", "محركات البحث", "كلمات مفتاحية", "تحسين محركات"):
        return "seo"
    if has(text, "تسويق", "مسوق", "إعلانات جوجل", "إعلانات فيسبوك", "مؤثرين", "علامة تجارية", "علاقات عامة", "مبيعات", "تجارة إلكترونية", "growth hacker", "سلوك مستهلك", "أبحاث سوق", "إدارة السمعة", "إعلان رقمي", "مدير حملات", "استهداف إعلاني", "تسويق بالمحتوى", "متجر إلكتروني", "تسويق عبر البريد"):
        return "marketing"
    if has(text, "خدمة عملاء", "دعم فني", "دعم العملاء", "تجربة عميل", "chatbot", "شات بوت", "شكاوى", "مركز اتصال", "إدارة علاقات العملاء", "cx "):
        return "support"
    if has(text, "البريد", "مراسلات", "سكرتير", "مساعد إداري", "مساعد تنفيذي", "كاتب رسائل"):
        return "email"
    if has(text, "إنتاجية", "إدارة وقت", "مدير وقت", "منظم مهام", "منظم حياة"):
        return "work"
    if has(text, "فيديو", "مونتاج", "مخرج", "بودكاست", "صوتيات", "هندسة صوت", "موسيقى", "سينمائي", "تحريك", "stop motion", "مؤثرات صوتية", "مصور فيديو"):
        return "video"
    if has(text, "مصمم", "تصميم جرافيك", "فنان", "رسام", "تصوير", "أزياء", "خطوط طباعية", "typography", "معماري", "تصميم داخلي", "رسوم", "ديكور", "جرافيك", "خطاط", "صانع مجوهرات", "صناعة الجلود"):
        return "image"
    if has(text, "محلل بيانات", "بيانات تسويقية", "علم بيانات", "محلل إحصائي", "إحصاء", "تعلم آلة", "ذكاء اصطناعي", "باحث في الذكاء", "محلل مالي", "محلل اقتصادي", "محلل توجهات", "إحصائي", "ذكاء الأعمال"):
        return "data"
    if has(text, "كاتب محتوى", "كاتب نصوص", "كاتب إعلاني", "صانع محتوى", "مدون", "محرر", "مقال", "محتوى", "صحفي", "نشرة", "كاتب", "روائي", "شاعر", "مسرحي", "مترجم", "مؤلف", "شاعر"):
        return "content"
    if has(text, "مدير مشاريع", "إدارة مشاريع", "مشاريع", "مستشار إداري", "استشاري إداري", "مدير عمليات", "محلل أعمال", "مستشار أعمال", "رائد أعمال", "ريادة الأعمال", "استراتيجية", "إدارة مخاطر", "مدير تنفيذي", "مستشار مالي", "محاسب", "اقتصاد", "مستشار", "مدير جودة", "مدير منتج", "سلاسل التوريد", "عمليات", "محلل ائتمان", "مدير خزينة", "محافظ استثمارية", "مدير ثروات", "تقييم شركات", "ميزانيات", "مخطط مالي", "مصرفي", "مصرفية", "إدارة ممتلكات", "تجارة تجزئة", "تسعير", "حوكمة", "امتثال", "مفاوض", "عقارات", "خبير أسواق", "استثمار", "تدقيق داخلي", "مخطط مالي"):
        return "business"
    if has(text, "مهندس برمجيات", "مطور", "مبرمج", "خبير أمن", "مختبر اختراق", "اختبار برمجيات", "linux", "شبكات", "سحابي", "قواعد بيانات", "تقني", "نظم", "تقنية", "تكنولوجيا", "robot", "روبوت", "بلوك", "iot", "أنظمة مدمجة", "أجهزة", "تحليل نظم", "مختص تقني", "حاسوب", "معلوماتية", "هاكر أخلاقي", "أمن سيبراني", "مدير خوادم", "تقنيات", "أنظمة تشغيل", "واجهات برمجة التطبيقات", "مهندس بيانات", "مطور تطبيقات", "مهندس اختبار", "DevOps", "مهندس شبكات", "مهندس سحابي", "مهندس نظم", "مهندس ذكاء اصطناعي"):
        return "code"
    return "other"


def make_title(act: str, prompt: str) -> str:
    first = re.split(r"[.؟!\n]", prompt.strip(), maxsplit=1)[0].strip()
    first = re.sub(r"^(?:قم\s+ب(?:ـ)?|اكتب|أنشئ|صمم|صمّم|اشرح|قدّم|قدم|اقترح|ضع|كيف\s+يمكنني|كيف\s+يمكن|ما\s+هي|ما\s+هو|حلل|حلّل|ناقش|قارن|لخص|لخّص|صغ|حدد|حدّد|اعرض|أعد|اصنع)\s*", "", first)
    if len(first) > 65:
        first = first[:64].rstrip(" ،:؛-") + "…"
    return first or act


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="JSON array of objects with act and prompt fields")
    args = parser.parse_args()
    incoming = json.loads(args.source.read_text(encoding="utf-8"))
    if not isinstance(incoming, list):
        raise ValueError("Source must be a JSON array")
    if any(not isinstance(x, dict) or not isinstance(x.get("act"), str) or not isinstance(x.get("prompt"), str) or not x["act"].strip() or not x["prompt"].strip() for x in incoming):
        raise ValueError("Every source record must have non-empty string fields: act and prompt")

    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    existing = data["prompts"]
    existing_prompts = {p["prompt"].strip() for p in existing}
    existing_titles = {p["title"].strip().casefold() for p in existing}
    seen_source: set[str] = set()
    additions = []
    for item in incoming:
        act, source_prompt = item["act"].strip(), item["prompt"].strip()
        prompt = f"تصرّف بصفتك {act}. {source_prompt}"
        if source_prompt in seen_source or prompt in existing_prompts:
            continue
        seen_source.add(source_prompt)
        title = make_title(act, source_prompt)
        if title.casefold() in existing_titles:
            title = f"{title} — {act}"
        suffix = 2
        base_title = title
        while title.casefold() in existing_titles:
            title = f"{base_title} ({suffix})"
            suffix += 1
        existing_titles.add(title.casefold())
        category = classify(act, source_prompt)
        additions.append({
            "category": category,
            "title": title,
            "prompt": prompt,
            "summary": f"مهمة موجهة إلى {act}؛ أرفق المعلومات والسياق اللازمين قبل الاستخدام.",
            "model": "نموذج لغوي متعدد الاستخدامات",
            "settings": "لا توجد إعدادات إلزامية؛ أرفق السياق والمواد المناسبة للمهمة.",
            "example": "مثال توضيحي: استبدل المطلوب في الموجّه ببيانات المهمة الفعلية.",
            "tip": "تحقق من الحقائق والإجراءات المهنية من مصدر موثوق، ولا تُدخل بيانات حساسة.",
            "id": max((p["id"] for p in existing), default=0) + len(additions) + 1,
        })
    data["prompts"].extend(additions)
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(additions)} unique records; catalog now has {len(data['prompts'])} prompts.")

if __name__ == "__main__":
    main()
