# AGOS Factory

> **مصنع الوكلاء** — البنية التي تُنتج وكلاء الحضارة عند الطلب، دون تخزين ملايين الملفات.

## لماذا هذا المجلد؟

فحص المستودع (انظر `INTEGRITY-REPORT.md` في الجذر) كشف أن **1,021 ملف** تحت
`agent_civilization/agents/specialists/` هي وكلاء **مُولَّدون مسبقاً وثابتون
(SIMULATED)** — كل ملف كائن Python منفصل يعيد نتائج مُبرمَجة يدوياً (`{"patterns":
["trend", "outlier"], "confidence": 0.87}`) بدون أي استدعاء LLM حقيقي. هذا
النموذج **لا يتوسّع**: لإنتاج مليون وكيل يجب كتابة مليون ملف على القرص،
واستيرادها جميعاً في الذاكرة عند الإقلاع.

`agos-factory` يحل هذه المشكلة عبر مبدأ مهني واحد:

> **الوكيل ليس ملفاً. الوكيل نسخة عابرة (ephemeral instance) من مخطط
> (Blueprint) مُعرَّف مرة واحدة.**

بدلاً من توليد كود لكل وكيل، نولّد **تعريفات (Blueprints)** لكل تخصص، ثم
`AgentFactory` تُنشئ نسخاً حقيقية من هذه المخططات عند الطلب — بالآلاف أو
بالملايين — عبر تجمّعات (pools) محدودة الحجم في الذاكرة، مع مُوسِّع تلقائي
(autoscaler) يقرر متى تُنشأ نسخ جديدة ومتى تُعاد نسخ خاملة إلى المجمّع.

## البنية

```
agos-factory/
├── README.md                     ← هذا الملف
├── factory/                      ← مصنع الوكلاء (ينتج ملايين الوكلاء عند الطلب)
│   ├── blueprint.py               مخطط الوكيل + سجل المخططات (Blueprint / BlueprintRegistry)
│   ├── agent.py                    FactoryAgent — النسخة العابرة الحقيقية (LLM + أدوات)
│   ├── metrics.py                  عدادات ذرية Thread-safe لقياس المصنع
│   ├── pool.py                     تجمّع وكلاء محدود الحجم لكل تخصص (تدوير، لا تسريب ذاكرة)
│   ├── autoscaler.py               خوارزمية توسّع تلقائي بحسب استخدام كل تجمّع
│   ├── factory.py                  الواجهة العلوية: spawn / spawn_batch / scale_to / shutdown
│   └── cli.py                      واجهة سطر أوامر لتشغيل عرض توضيحي حقيقي
├── 01-AGL-Language/               ← لغة AGOS الوصفية (AGL)
│   ├── README.md                   المواصفة اللغوية (موجودة سابقاً)
│   ├── agl/                        المُحلِّل والمُصرِّف الحقيقي لِـ .agl
│   │   ├── lexer.py                 المُجزِّئ اللغوي (Tokenizer)
│   │   ├── ast_nodes.py             عناصر شجرة التركيب النحوي
│   │   ├── parser.py                المحلل النحوي التنازلي التكراري
│   │   ├── codegen_python.py        مولّد كلاسات Python (dataclass) حقيقية
│   │   ├── codegen_jsonschema.py    مولّد JSON Schema حقيقي
│   │   └── compiler.py              الواجهة العلوية: compile_source / compile_file
│   ├── examples/
│   │   └── mission.agl              نفس مثال Mission الوارد في README الأصلي
│   └── cli.py                      واجهة سطر أوامر: `python -m agos-factory... agl compile`
└── tests/
    ├── test_agl.py                  اختبارات حقيقية للمحلل والمصرّف
    └── test_factory.py              اختبارات حقيقية للمصنع والتوسّع التلقائي
```

## مبدأ التصميم: كيف "نُنتج ملايين الوكلاء" فعلياً؟

إنشاء مليون كائن Python فعلي في نفس اللحظة في الذاكرة غير واقعي مهنياً (كل
وكيل يحمل جلسة HTTP، سياق LLM، إحصائيات — استهلاك ذاكرة حقيقي). الحل المهني
المتبع في كل الأنظمة الموزَّعة الحقيقية (Kubernetes HPA، connection pools،
thread pools) هو:

1. **Blueprint واحد لكل تخصص** — مصدر الحقيقة الوحيد لِـ system prompt والأداة
   المرتبطة به وحدود التزامن.
2. **Pool محدود لكل تخصص** — عدد صغير من الوكلاء الفعليين النشطين (`max_concurrency`)
   يُعاد استخدامهم لملايين المهام المتتالية.
3. **Factory.spawn_batch()** — دالة async generator تُنفِّذ N مهمة (N يمكن أن
   تكون بالملايين) عبر الـ pool، وتُخرِج النتائج واحدة تلو الأخرى (streaming)
   دون الاحتفاظ بكل الوكلاء أو كل النتائج في الذاكرة دفعة واحدة.
4. **Autoscaler** — يرصد نسبة الانتظار في كل تجمّع ويزيد/يُقلّص حجمه ضمن حدود
   موارد معقولة (`min_size` / `max_size`)، بدل تثبيت رقم عشوائي.
5. **العداد التراكمي (`FactoryMetrics.total_spawned`)** — هو العدد الحقيقي
   لعمليات إنشاء الوكلاء منذ الإقلاع، ويمكن أن يتجاوز الملايين دون أن يعني ذلك
   وجود مليون كائن حيّ في الذاكرة في آنٍ واحد.

بهذا، جملة "الحضارة تُنتج ملايين الوكلاء حسب الحاجة" تصبح **حقيقة تشغيلية
قابلة للقياس** (`factory.metrics.snapshot()`)، لا رقماً تسويقياً.

## الاستخدام السريع

```python
import asyncio
from agos_factory_pkg import AgentFactory, BlueprintRegistry

async def main():
    registry = BlueprintRegistry.from_agent_civilization()  # يقرأ التخصصات الحقيقية
    factory = AgentFactory(registry)

    # وكيل واحد فوري
    agent = await factory.spawn("analyst")
    result = await agent.execute({"prompt": "حلل اتجاه المبيعات الشهرية"})

    # دفعة كبيرة (تصل للملايين) بدون استهلاك ذاكرة غير منضبط
    async for outcome in factory.spawn_batch("researcher", prompts=[f"سؤال {i}" for i in range(2000)]):
        pass

    print(factory.metrics.snapshot())
    await factory.shutdown()

asyncio.run(main())
```

راجع `factory/cli.py` لتشغيل عرض توضيحي حقيقي من سطر الأوامر:

```bash
python -m agos_factory_pkg.cli demo --spec analyst --count 5000 --concurrency 25
```

## AGL — من التعريف إلى الكود تلقائياً

```bash
python -m agos_factory_pkg.agl.cli compile 01-AGL-Language/examples/mission.agl -o /tmp/out
# ينتج: Mission.py (dataclass حقيقي) و Mission.schema.json (JSON Schema حقيقي)
```

## التكامل مع الحضارة القائمة

- `BlueprintRegistry.from_agent_civilization()` يستورد `SPECIALIZATIONS` و
  `SPECIALIZATION_TOOLS` الحقيقية من `agent_civilization.agents.real.real_agents`
  — لا يُعاد تعريف أي system prompt، بل يُعاد استخدامه كما هو.
- `FactoryAgent.execute()` يستخدم نفس `agent_civilization.core.llm.get_llm()`
  المُهيَّأ بمفتاح `OPENROUTER_API_KEY` — نفس مسار الذكاء الحقيقي في `server.py`.
- يمكن ربط `AgentFactory` بـ `server.py` مباشرة عبر استبدال
  `create_civilization()` بـ `factory.spawn(specialization)` لكل مهمة واردة،
  بدل تثبيت عدد الوكلاء عند الإقلاع (`AGENTS_PER_SPEC`).
