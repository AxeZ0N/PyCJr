## 2026-08-30 · IRPING2_MIN · result

```json
{
"id": "IRPING2_MIN",
"contract": {
  "source": "BASLOAD.BAS + IRPING2.ASM",
  "expected": { "return": "RETURNED OK", "result_byte": 3 },
  "regression": "self (transport-only); CH0CAL stays functional primary",
  "recovery": "cold_power_cycle"
},
"result": {
  "loaded": 56,
  "return": "RETURNED OK",
  "result_byte": 3,
  "keyboard": "intact",
  "rising": 0,
  "falling": 0,
  "note": "rising/falling are meaningless on this probe; it writes only O+128."
},
"verdict": "pass"
}
```

