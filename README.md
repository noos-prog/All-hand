# AGOS Agent Civilization

حضارة وكلاء ذكاء اصطناعي حقيقية: 20 تخصص × N وكلاء يعملون بنماذج LLM وأدوات فعلية لخدمة المستخدم والحضارة.

## المميزات

- **20 تخصص حقيقي**: محلل، مهندس، مبرمج، باحث، مراقب، وغيرها — كل وكيل يستخدم LLM (OpenRouter) مع أدوات فعلية
- **أدوات فعلية**: بحث ويب مباشر (DuckDuckGo)، إحصائيات حقيقية، تنفيذ كود Python، التحقق من JSON، مراقبة النظام
- **قاعدة بيانات Supabase**: حفظ المهام، إحصائيات الوكلاء، وسجل الأحداث
- **واجهة ويب متجاوبة**: محادثة، لوحة تحكم، إدارة التخصصات والوكلاء، وتتبع المهام
- **تحديثات مباشرة (SSE)**: أحداث في الوقت الفعلي عند إنشاء وإكمال المهام
- **وكلاء خارجيون**: إضافة أي وكيل يدعم OpenAI-compatible API (Ollama, vLLM, LM Studio)
- **مخططط للنشر على Render**: Dockerfile + render.yaml جاهزة

## البنية

```
project/
├── server.py                          # خادم FastAPI - نقطة الدخول
├── run.py                             # وضع تفاعلي (بدون خادم)
├── agent_civilization/
│   ├── core/
│   │   ├── llm.py                    # عميل OpenRouter LLM
│   │   └── agents/
│   │       ├── base_agent.py         # الوكيل الأساسي
│   │       └── communication_hub.py  # محور التواصل بين الوكلاء
│   ├── agents/
│   │   ├── real/
│   │   │   └── real_agents.py        # 20 تخصص + أدوات حقيقية
│   │   ├── external_adapter.py       # محول الوكلاء الخارجيين
│   │   ├── infrastructure/
│   │   │   ├── orchestrator_agent.py # المنسق
│   │   │   ├── task_dispatcher.py    # موزع المهام
│   │   │   └── resource_manager.py   # مدير الموارد
│   │   └── executors/
│   │       └── data_worker.py        # عامل بيانات
│   └── storage/
│       └── supabase_store.py          # طبقة حفظ Supabase
├── web/                               # واجهة React (Vite)
│   ├── src/
│   │   ├── App.jsx                   # التطبيق الرئيسي
│   │   ├── api.js                    # عميل API
│   │   ├── components/
│   │   │   ├── Dashboard.jsx         # لوحة التحكم
│   │   │   ├── Chat.jsx              # المحادثة
│   │   │   ├── Specializations.jsx   # التخصصات
│   │   │   ├── Agents.jsx            # الوكلاء
│   │   │   └── Tasks.jsx             # المهام
│   │   └── index.css                 # الأنماط
│   └── vite.config.js
├── Dockerfile                         # بناء متعدد المراحل (frontend + backend)
├── render.yaml                        # إعدادات Render
├── requirements.txt                   # مكتبات Python
└── .env.example                       # مثال لمتغيرات البيئة
```

## التشغيل المحلي

```bash
# 1. تثبيت مكتبات Python
pip install -r requirements.txt

# 2. بناء الواجهة
cd web && npm install && npm run build && cd ..

# 3. تشغيل الخادم
uvicorn server:app --reload --port 8000
```

أو وضع تفاعلي بدون خادم:
```bash
python run.py
```

## النشر على Render

1. اربط المستودع بـ Render
2. استخدم `render.yaml` كـ Blueprint
3. أضف متغيرات البيئة:
   - `OPENROUTER_API_KEY` — مفتاح OpenRouter (مطلوب للذكاء)
   - `SUPABASE_URL` و `SUPABASE_ANON_KEY` — لقاعدة البيانات
   - `VITE_SUPABASE_URL` و `VITE_SUPABASE_ANON_KEY` — نفس القيم

## API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api` | GET | معلومات النظام |
| `/api/system/status` | GET | حالة النظام |
| `/api/specializations` | GET | قائمة التخصصات |
| `/api/agents` | GET | قائمة الوكلاء |
| `/api/tasks` | GET/POST | المهام |
| `/api/chat` | POST | محادثة بلغة طبيعية |
| `/api/events` | GET | سجل الأحداث |
| `/api/events/stream` | GET | SSE مباشر |
| `/api/agents/external` | POST/DELETE | إدارة الوكلاء الخارجيين |
| `/docs` | GET | توثيق OpenAPI |
