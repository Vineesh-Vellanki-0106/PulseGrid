\# ⚡ PulseGrid



\## Decentralized Multi-Agent Emergency Response Optimization



PulseGrid is a decentralized multi-agent simulation system designed for emergency response in dynamic environments.



The system coordinates autonomous response agents using local task bidding, heuristic allocation, A\* trajectory planning, collision detection, dynamic replanning, communication resilience, and decentralized failure recovery.



The implementation is designed for the \*\*IEEE EMBS OptiForge Hackathon — Intelligent Systems \& Autonomous Computing\*\* track.



\---



\# 1. Problem



Emergency response systems operate in environments where:



\- multiple agents compete for tasks,

\- obstacles can appear dynamically,

\- communication can become unavailable,

\- individual agents can fail,

\- routes must be recalculated quickly,

\- collisions and deadlocks must be minimized.



A centralized controller introduces a potential single point of failure.



PulseGrid instead uses decentralized agent-level decision making.



\---



\# 2. Core Architecture



```text

&#x20;                   ENVIRONMENT

&#x20;                        │

&#x20;                        ▼

&#x20;                 LOCAL AGENT STATE

&#x20;                        │

&#x20;                        ▼

&#x20;                 TASK COST / BID

&#x20;                        │

&#x20;                        ▼

&#x20;             DECENTRALIZED ALLOCATION

&#x20;                        │

&#x20;                        ▼

&#x20;                  A\* PATH PLANNING

&#x20;                        │

&#x20;                        ▼

&#x20;                COLLISION DETECTION

&#x20;                        │

&#x20;                        ▼

&#x20;                     EXECUTION

&#x20;                        │

&#x20;             ┌──────────┴──────────┐

&#x20;             │                     │

&#x20;       ENVIRONMENTAL           AGENT FAILURE

&#x20;       PERTURBATION                  │

&#x20;             │                       │

&#x20;             ▼                       ▼

&#x20;         REPLANNING             TASK RECOVERY

&#x20;             │                       │

&#x20;             └──────────┬────────────┘

&#x20;                        ▼

&#x20;                   METRICS

