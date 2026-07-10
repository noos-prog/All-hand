# نشر حضارة الوكلاء على Render (مجاناً)

## الخطوات

1. أنشئ حساباً مجانياً على [render.com](https://render.com)
2. اضغط **New → Blueprint** واربط مستودع GitHub هذا (`reeveero-tech/All-hand`)
3. Render سيقرأ `render.yaml` تلقائياً وينشئ الخدمة
4. أدخل قيمة `OPENROUTER_API_KEY`:
   - أنشئ مفتاحاً مجانياً من [openrouter.ai/keys](https://openrouter.ai/keys)
   - النموذج الافتراضي `meta-llama/llama-3.3-70b-instruct:free` **مجاني بالكامل**
5. انتظر اكتمال النشر — رابطك سيكون مثل: `https://agos-civilization.onrender.com`

## التحقق

```bash
curl https://YOUR-APP.onrender.com/system/status
```

## نقاط النهاية

| Endpoint | الوظيفة |
|---|---|
| `GET /system/status` | صحة الحضارة |
| `GET /agents` | قائمة الوكلاء |
| `GET /specializations` | التخصصات الـ20 |
| `POST /tasks` | إرسال مهمة `{specialization, prompt, data?}` |
| `GET /tasks/{id}` | نتيجة المهمة |
| `POST /chat` | أمر بلغة طبيعية → يُوجَّه تلقائياً للوكيل الأنسب |
| `POST /agents/external` | ربط وكيل خارجي مفتوح المصدر (OpenAI-compatible) |
| `GET /docs` | توثيق تفاعلي (Swagger) |

## متغيرات البيئة

| المتغير | الوصف | افتراضي |
|---|---|---|
| `OPENROUTER_API_KEY` | مفتاح LLM (مطلوب للذكاء الحقيقي) | — |
| `LLM_MODEL` | النموذج المستخدم | `meta-llama/llama-3.3-70b-instruct:free` |
| `AGENTS_PER_SPEC` | عدد الوكلاء لكل تخصص (50 = 1000 وكيل) | `5` |
| `EXTERNAL_AGENTS` | JSON لوكلاء خارجيين يُحمَّلون عند الإقلاع | — |

## التشغيل محلياً

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY=sk-or-...
uvicorn server:app --reload
```
