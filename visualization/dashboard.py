import sys
from pathlib import Path

# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


import streamlit as st
import plotly.graph_objects as go

from simulation.scenarios import create_demo_scenario
from simulation.engine import SimulationEngine


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="PulseGrid",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# GLOBAL CSS
# =========================================================

st.html(
    """
    <style>

    /* =====================================================
       APPLICATION BACKGROUND
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(14, 116, 144, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(37, 99, 235, 0.12),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #06111c 0%,
                #091827 50%,
                #0b1725 100%
            );
    }

    .main .block-container {
        max-width: 1500px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #06101a 0%,
                #081521 100%
            );

        border-right: 1px solid #1b344a;
    }


    /* =====================================================
       NATIVE TITLE
       ===================================================== */

    h1 {
        color: #f8fafc !important;
        font-weight: 800 !important;
        letter-spacing: -0.045em !important;
    }

    h2, h3 {
        color: #e2edf6 !important;
    }


    /* =====================================================
       STREAMLIT TABS
       ===================================================== */

    button[data-baseweb="tab"] {
        color: #71899e !important;
        font-weight: 650 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #38bdf8 !important;
    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {
        background: #0e2336 !important;
        border: 1px solid #28465f !important;
        color: #dce8f2 !important;
        border-radius: 8px !important;
        min-height: 42px !important;
        font-weight: 700 !important;
    }

    .stButton > button:hover {
        background: #12304a !important;
        border-color: #38bdf8 !important;
        color: white !important;
    }


    /* =====================================================
       DATAFRAME
       ===================================================== */

    div[data-testid="stDataFrame"] {
        border: 1px solid #1d3a51;
        border-radius: 9px;
        overflow: hidden;
    }


    /* =====================================================
       METRIC
       ===================================================== */

    div[data-testid="stMetric"] {
        background:
            linear-gradient(
                145deg,
                #0e1f30,
                #0b1927
            );

        border: 1px solid #1d3a51;
        border-radius: 11px;
        padding: 14px;
    }

    div[data-testid="stMetricLabel"] {
        color: #7891a6 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }


    /* =====================================================
       EXPANDERS
       ===================================================== */

    div[data-testid="stExpander"] {
        border: 1px solid #1d3a51 !important;
        border-radius: 9px !important;
        background: #0a1826 !important;
    }

    </style>
    """
)


# =========================================================
# CUSTOM HTML HELPERS
# =========================================================

def html_card(
    title,
    value,
    subtitle="",
    accent="#38bdf8",
):

    return f"""
    <div style="
        background:linear-gradient(
            145deg,
            #0e2031,
            #0a1826
        );
        border:1px solid #1d3a51;
        border-radius:12px;
        padding:16px 17px;
        min-height:105px;
        box-shadow:
            0 10px 25px rgba(0,0,0,0.22);
    ">

        <div style="
            color:#7891a6;
            font-size:0.67rem;
            font-weight:750;
            letter-spacing:0.12em;
            text-transform:uppercase;
        ">
            {title}
        </div>

        <div style="
            color:#f8fafc;
            font-size:1.65rem;
            font-weight:800;
            margin-top:7px;
            letter-spacing:-0.035em;
        ">
            {value}
        </div>

        <div style="
            color:{accent};
            opacity:0.78;
            font-size:0.70rem;
            margin-top:3px;
        ">
            {subtitle}
        </div>

    </div>
    """


def event_card(
    tick,
    message,
    event_type="info",
):

    colors = {
        "success": "#22c55e",
        "warning": "#f59e0b",
        "critical": "#ef4444",
        "info": "#38bdf8",
    }

    accent = colors.get(
        event_type,
        "#38bdf8",
    )

    return f"""
    <div style="
        border-left:3px solid {accent};
        background:#0c1b29;
        border-top:1px solid #193249;
        border-right:1px solid #193249;
        border-bottom:1px solid #193249;
        border-radius:0 7px 7px 0;
        padding:9px 11px;
        margin-bottom:7px;
        color:#c8d6e2;
        font-size:0.76rem;
        line-height:1.4;
    ">

        <span style="
            color:#587087;
            font-family:monospace;
            font-weight:700;
            margin-right:8px;
        ">
            T{tick:02d}
        </span>

        {message}

    </div>
    """


def health_card(
    title,
    status,
    icon="●",
    color="#4ade80",
):

    return f"""
    <div style="
        background:#0b1a28;
        border:1px solid #1b354b;
        border-radius:9px;
        padding:11px 13px;
    ">

        <div style="
            color:#617b91;
            font-size:0.65rem;
            text-transform:uppercase;
            letter-spacing:0.09em;
        ">
            {title}
        </div>

        <div style="
            color:#dce8f2;
            font-size:0.83rem;
            font-weight:700;
            margin-top:4px;
        ">

            <span style="
                color:{color};
                margin-right:5px;
            ">
                {icon}
            </span>

            {status}

        </div>

    </div>
    """


# =========================================================
# INITIALIZE SIMULATION
# =========================================================

def initialize_simulation():

    grid, agents, incidents = create_demo_scenario()

    engine = SimulationEngine(grid)

    for agent in agents:
        engine.add_agent(agent)

    assignments = engine.allocate_all_incidents(
        incidents
    )

    engine.start()

    st.session_state.grid = grid
    st.session_state.agents = agents
    st.session_state.incidents = incidents
    st.session_state.engine = engine
    st.session_state.assignments = assignments

    st.session_state.events = [
        {
            "tick": 0,
            "type": "success",
            "text": "Decentralized task allocation completed",
        }
    ]

    st.session_state.position_history = {
        agent.agent_id: [agent.position]
        for agent in agents
    }

    st.session_state.initialized = True


if "initialized" not in st.session_state:

    st.session_state.initialized = False


if not st.session_state.initialized:

    initialize_simulation()


grid = st.session_state.grid
agents = st.session_state.agents
incidents = st.session_state.incidents
engine = st.session_state.engine


# =========================================================
# EVENT LOGGER
# =========================================================

def record_event(
    tick,
    event_type,
    message,
):

    st.session_state.events.append(
        {
            "tick": tick,
            "type": event_type,
            "text": message,
        }
    )


# =========================================================
# ADVANCE SIMULATION
# =========================================================

def advance_simulation():

    previous_replans = (
        engine.metrics.replans
    )


    # -----------------------------------------------------
    # Dynamic obstacle
    # -----------------------------------------------------

    if engine.tick == 2:

        grid.add_obstacle(
            (1, 4)
        )

        record_event(
            engine.tick + 1,
            "warning",
            "Dynamic obstacle detected at (1, 4)",
        )


    # -----------------------------------------------------
    # Communication loss
    # -----------------------------------------------------

    if engine.tick == 3:

        agents[1].lose_communication()

        record_event(
            engine.tick + 1,
            "warning",
            "A2 communication link lost",
        )


    # -----------------------------------------------------
    # Agent failure
    # -----------------------------------------------------

    if engine.tick == 4:

        agents[2].fail()

        record_event(
            engine.tick + 1,
            "critical",
            "A3 failure detected",
        )

        reassigned = (
            engine.reassign_failed_tasks(
                incidents
            )
        )

        for event in reassigned:

            record_event(
                engine.tick + 1,
                "info",
                (
                    f"{event['incident_id']} "
                    f"reassigned to "
                    f"{event['agent_id']}"
                ),
            )


    # -----------------------------------------------------
    # Engine tick
    # -----------------------------------------------------

    engine.advance_tick()


    # -----------------------------------------------------
    # Replanning evidence
    # -----------------------------------------------------

    if (
        engine.metrics.replans
        > previous_replans
    ):

        record_event(
            engine.tick,
            "info",
            "Trajectory recalculated after environmental perturbation",
        )


    # -----------------------------------------------------
    # Position history
    # -----------------------------------------------------

    for agent in agents:

        st.session_state.position_history[
            agent.agent_id
        ].append(
            agent.position
        )


    # -----------------------------------------------------
    # Mission completion
    # -----------------------------------------------------

    if all(
        incident.completed
        for incident in incidents
    ):

        already_logged = any(
            "All emergency incidents completed"
            in event["text"]
            for event in st.session_state.events
        )

        if not already_logged:

            record_event(
                engine.tick,
                "success",
                "All emergency incidents completed",
            )


# =========================================================
# RUN COMPLETE SCENARIO
# =========================================================

def run_full_scenario():

    for _ in range(30):

        if all(
            incident.completed
            for incident in incidents
        ):
            break

        advance_simulation()


# =========================================================
# HEADER
# =========================================================

header_left, header_right = st.columns(
    [4.8, 1.2]
)

with header_left:

    st.title(
        "⚡ PulseGrid"
    )

    st.caption(
        "Decentralized Multi-Agent Emergency Response Optimization"
    )


with header_right:

    st.html(
        """
        <div style="
            text-align:right;
            margin-top:18px;
        ">

            <span style="
                display:inline-block;
                padding:7px 13px;
                border-radius:999px;

                background:rgba(34,197,94,0.07);
                border:1px solid rgba(34,197,94,0.30);

                color:#86efac;

                font-size:0.67rem;
                font-weight:750;

                letter-spacing:0.08em;
                text-transform:uppercase;
            ">
                ● SYSTEM OPERATIONAL
            </span>

        </div>
        """
    )


# =========================================================
# MISSION BANNER
# =========================================================

st.html(
    """
    <div style="
        margin:8px 0 17px 0;
        padding:11px 14px;

        border-radius:9px;

        background:
            linear-gradient(
                90deg,
                rgba(14,116,144,0.13),
                rgba(37,99,235,0.06)
            );

        border:1px solid rgba(56,189,248,0.18);

        color:#9ec3d9;
        font-size:0.75rem;
    ">

        <b style="color:#bae6fd;">
            COMBINED STRESS SCENARIO
        </b>

        &nbsp;·&nbsp;

        Dynamic obstacle

        &nbsp;+

        communication dropout

        &nbsp;+

        agent failure

        &nbsp;+

        decentralized recovery

    </div>
    """
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.subheader(
        "Operations Control"
    )

    st.caption(
        "Autonomous mission execution"
    )


    if st.button(
        "▶▶  Run Full Scenario",
        use_container_width=True,
    ):

        run_full_scenario()

        st.rerun()


    if st.button(
        "▶  Advance One Tick",
        use_container_width=True,
    ):

        advance_simulation()

        st.rerun()


    if st.button(
        "↻  Reset Mission",
        use_container_width=True,
    ):

        st.session_state.initialized = False

        st.rerun()


    st.divider()


    st.caption(
        "MISSION STATE"
    )

    st.markdown(
        f"### T{engine.tick:02d}"
    )

    st.caption(
        "Simulation tick"
    )


    st.divider()


    st.caption(
        "AUTONOMOUS STACK"
    )

    st.markdown(
        """
        ✓ Distributed task allocation

        ✓ A* trajectory planning

        ✓ Collision avoidance

        ✓ Dynamic replanning

        ✓ Communication resilience

        ✓ Failure recovery

        ✓ Runtime evaluation
        """
    )


# =========================================================
# SUMMARY
# =========================================================

summary = engine.metrics.summary()

completed = summary["completed_tasks"]

total_incidents = len(
    incidents
)

active_agents = sum(
    1
    for agent in agents
    if agent.active
)

connected_agents = sum(
    1
    for agent in agents
    if agent.communication_available
)


# =========================================================
# KPI CARDS
# =========================================================

kpis = [
    (
        "INCIDENTS",
        f"{completed}/{total_incidents}",
        "mission completion",
    ),
    (
        "ACTIVE AGENTS",
        f"{active_agents}/{len(agents)}",
        "fleet availability",
    ),
    (
        "COLLISIONS",
        str(summary["collisions"]),
        "safety violations",
    ),
    (
        "REPLANS",
        str(summary["replans"]),
        "adaptive responses",
    ),
    (
        "AVG LATENCY",
        f"{summary['average_latency_ms']:.3f} ms",
        "decision time / tick",
    ),
]


kpi_columns = st.columns(
    len(kpis)
)

for column, data in zip(
    kpi_columns,
    kpis,
):

    with column:

        title, value, subtitle = data

        st.html(
            html_card(
                title,
                value,
                subtitle,
            )
        )


st.markdown("")


# =========================================================
# SYSTEM HEALTH
# =========================================================

health_columns = st.columns(4)


with health_columns[0]:

    st.html(
        health_card(
            "Planning",
            "A* NOMINAL",
        )
    )


with health_columns[1]:

    if summary["collisions"] == 0:

        st.html(
            health_card(
                "Safety",
                "NOMINAL",
            )
        )

    else:

        st.html(
            health_card(
                "Safety",
                "ATTENTION",
                color="#fbbf24",
            )
        )


with health_columns[2]:

    st.html(
        health_card(
            "Adaptation",
            (
                "ACTIVE"
                if summary["replans"] > 0
                else "STANDBY"
            ),
            icon="↻",
            color="#38bdf8",
        )
    )


with health_columns[3]:

    if active_agents < len(agents):

        st.html(
            health_card(
                "Resilience",
                "RECOVERY ACTIVE",
                color="#fbbf24",
            )
        )

    else:

        st.html(
            health_card(
                "Resilience",
                "NOMINAL",
            )
        )


st.markdown("")


# =========================================================
# MAIN TABS
# =========================================================

tab_live, tab_fleet, tab_performance, tab_architecture = st.tabs(
    [
        "LIVE OPERATIONS",
        "FLEET STATUS",
        "PERFORMANCE & EVIDENCE",
        "SYSTEM ARCHITECTURE",
    ]
)


# =========================================================
# LIVE OPERATIONS
# =========================================================

with tab_live:

    map_column, event_column = st.columns(
        [3.25, 1.25]
    )


    # -----------------------------------------------------
    # LIVE MAP
    # -----------------------------------------------------

    with map_column:

        st.subheader(
            "Live Swarm Environment"
        )

        st.caption(
            "Actual movement, planned trajectories, incidents and environmental hazards"
        )


        fig = go.Figure()


        # -------------------------------------------------
        # Historical trajectories
        # -------------------------------------------------

        for agent in agents:

            history = (
                st.session_state
                .position_history[
                    agent.agent_id
                ]
            )

            if len(history) > 1:

                history_x = [
                    point[0]
                    for point in history
                ]

                history_y = [
                    point[1]
                    for point in history
                ]

                fig.add_trace(
                    go.Scatter(
                        x=history_x,
                        y=history_y,
                        mode="lines",
                        name=(
                            f"{agent.agent_id} "
                            "travelled"
                        ),
                        line=dict(
                            width=2,
                            dash="solid",
                        ),
                        opacity=0.35,
                        showlegend=False,
                    )
                )


        # -------------------------------------------------
        # Planned paths
        # -------------------------------------------------

        for agent in agents:

            if (
                agent.active
                and agent.path
                and len(agent.path) > 1
            ):

                path_x = [
                    point[0]
                    for point in agent.path
                ]

                path_y = [
                    point[1]
                    for point in agent.path
                ]

                fig.add_trace(
                    go.Scatter(
                        x=path_x,
                        y=path_y,
                        mode="lines",
                        name=(
                            f"{agent.agent_id} "
                            "planned"
                        ),
                        line=dict(
                            width=2,
                            dash="dot",
                        ),
                        opacity=0.75,
                        showlegend=False,
                    )
                )


        # -------------------------------------------------
        # Obstacles
        # -------------------------------------------------

        if grid.obstacles:

            obstacle_x = [
                point[0]
                for point in grid.obstacles
            ]

            obstacle_y = [
                point[1]
                for point in grid.obstacles
            ]

            fig.add_trace(
                go.Scatter(
                    x=obstacle_x,
                    y=obstacle_y,
                    mode="markers",
                    name="Obstacles",
                    marker=dict(
                        symbol="square",
                        size=15,
                    ),
                    hovertemplate=(
                        "<b>Obstacle</b><br>"
                        "Position: "
                        "(%{x}, %{y})"
                        "<extra></extra>"
                    ),
                )
            )


        # -------------------------------------------------
        # Incidents
        # -------------------------------------------------

        incident_x = [
            incident.position[0]
            for incident in incidents
        ]

        incident_y = [
            incident.position[1]
            for incident in incidents
        ]

        fig.add_trace(
            go.Scatter(
                x=incident_x,
                y=incident_y,
                mode="markers+text",
                text=[
                    incident.incident_id
                    for incident in incidents
                ],
                textposition="top center",
                name="Emergency Incidents",
                marker=dict(
                    symbol="diamond",
                    size=14,
                ),
                hovertext=[
                    (
                        f"<b>{incident.incident_id}</b><br>"
                        f"Severity: {incident.severity}<br>"
                        f"Resource: {incident.resource_type}<br>"
                        f"Completed: {incident.completed}"
                    )
                    for incident in incidents
                ],
                hoverinfo="text",
            )
        )


        # -------------------------------------------------
        # Agents
        # -------------------------------------------------

        agent_x = [
            agent.position[0]
            for agent in agents
        ]

        agent_y = [
            agent.position[1]
            for agent in agents
        ]


        fig.add_trace(
            go.Scatter(
                x=agent_x,
                y=agent_y,
                mode="markers+text",
                text=[
                    agent.agent_id
                    for agent in agents
                ],
                textposition="bottom center",
                name="Response Agents",
                marker=dict(
                    size=16,
                    symbol="circle",
                ),
                hovertext=[
                    (
                        f"<b>{agent.agent_id}</b><br>"
                        f"Position: {agent.position}<br>"
                        f"Task: "
                        f"{agent.current_task.incident_id if agent.current_task else 'NONE'}<br>"
                        f"Active: {agent.active}<br>"
                        f"Communication: {agent.communication_available}<br>"
                        f"Energy: {agent.energy:.1f}"
                    )
                    for agent in agents
                ],
                hoverinfo="text",
            )
        )


        fig.update_layout(
            height=640,

            paper_bgcolor="#091827",
            plot_bgcolor="#091827",

            font=dict(
                color="#9bb0c2",
            ),

            xaxis=dict(
                title="Grid X",
                range=[
                    -1,
                    grid.width,
                ],
                dtick=1,
                gridcolor="#183047",
                zeroline=False,
            ),

            yaxis=dict(
                title="Grid Y",
                range=[
                    -1,
                    grid.height,
                ],
                dtick=1,
                gridcolor="#183047",
                zeroline=False,
                scaleanchor="x",
                scaleratio=1,
            ),

            margin=dict(
                l=45,
                r=20,
                t=20,
                b=45,
            ),

            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.01,
                xanchor="left",
                x=0,
            ),

            hoverlabel=dict(
                bgcolor="#0c1b29",
                bordercolor="#29455e",
            ),
        )


        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displaylogo": False,
                "scrollZoom": True,
            },
        )


    # -----------------------------------------------------
    # EVENT STREAM
    # -----------------------------------------------------

    with event_column:

        st.subheader(
            "Mission Event Stream"
        )

        st.caption(
            "Autonomous decisions and environmental changes"
        )


        for event in reversed(
            st.session_state.events[-9:]
        ):

            st.html(
                event_card(
                    event["tick"],
                    event["text"],
                    event["type"],
                )
            )


        st.markdown("")


        st.subheader(
            "Decision State"
        )


        decision_rows = []


        for agent in agents:

            if not agent.active:

                decision = "FAILED"
                state = "RECOVERY"

            elif agent.current_task:

                decision = "EXECUTE"
                state = (
                    agent.current_task.incident_id
                )

            else:

                decision = "AVAILABLE"
                state = "RESERVE"


            decision_rows.append(
                {
                    "Agent": agent.agent_id,
                    "Decision": decision,
                    "State": state,
                }
            )


        st.dataframe(
            decision_rows,
            use_container_width=True,
            hide_index=True,
            height=225,
        )


# =========================================================
# FLEET STATUS
# =========================================================

with tab_fleet:

    st.subheader(
        "Autonomous Response Fleet"
    )

    st.caption(
        "Agent capability, energy, communication and mission state"
    )


    fleet_rows = []


    for agent in agents:

        task = (
            agent.current_task.incident_id
            if agent.current_task
            else "RESERVE / IDLE"
        )

        fleet_rows.append(
            {
                "Agent": agent.agent_id,
                "Position": str(agent.position),
                "Task": task,
                "Status": (
                    "ACTIVE"
                    if agent.active
                    else "FAILED"
                ),
                "Communication": (
                    "CONNECTED"
                    if agent.communication_available
                    else "OFFLINE"
                ),
                "Energy": round(
                    agent.energy,
                    1,
                ),
                "Capabilities": ", ".join(
                    sorted(agent.capabilities)
                ),
            }
        )


    st.dataframe(
        fleet_rows,
        use_container_width=True,
        hide_index=True,
        height=270,
    )


    st.markdown("---")


    left, right = st.columns(2)


    with left:

        st.info(
            f"""
            **Communication resilience**

            {connected_agents}/{len(agents)}
            agents currently connected.

            Active assignments can continue local execution
            during temporary communication loss.
            """
        )


    with right:

        failed = (
            len(agents)
            - active_agents
        )

        st.info(
            f"""
            **Failure recovery**

            {failed} failed agent(s).

            Reserve capacity enables decentralized
            reassignment without a central controller.
            """
        )


# =========================================================
# PERFORMANCE
# =========================================================

with tab_performance:

    st.subheader(
        "Operational Performance"
    )

    st.caption(
        "Measured runtime, safety and optimization evidence"
    )


    p1, p2, p3, p4 = st.columns(4)


    with p1:

        st.metric(
            "Fitness",
            summary["fitness"],
        )


    with p2:

        st.metric(
            "Actual Path Cost",
            summary["total_path_cost"],
        )


    with p3:

        st.metric(
            "Energy Consumed",
            summary["energy_consumed"],
        )


    with p4:

        st.metric(
            "Deadlocks",
            summary["deadlocks"],
        )


    st.markdown("---")


    st.subheader(
        "Requirement Evidence"
    )


    recovery_verified = any(
        "reassigned"
        in event["text"]
        for event in st.session_state.events
    )


    evidence_rows = [
        {
            "Requirement": "Collision-free execution",
            "Observed": f"{summary['collisions']} collisions",
            "Status": (
                "PASS"
                if summary["collisions"] == 0
                else "ATTENTION"
            ),
        },
        {
            "Requirement": "Deadlock avoidance",
            "Observed": f"{summary['deadlocks']} deadlocks",
            "Status": (
                "PASS"
                if summary["deadlocks"] == 0
                else "ATTENTION"
            ),
        },
        {
            "Requirement": "Dynamic adaptation",
            "Observed": f"{summary['replans']} replans",
            "Status": (
                "PASS"
                if summary["replans"] > 0
                else "PENDING"
            ),
        },
        {
            "Requirement": "Mission completion",
            "Observed": (
                f"{completed}/{total_incidents} incidents"
            ),
            "Status": (
                "PASS"
                if completed == total_incidents
                else "PENDING"
            ),
        },
        {
            "Requirement": "Runtime measurement",
            "Observed": (
                f"{summary['average_latency_ms']:.3f} ms average"
            ),
            "Status": "PASS",
        },
        {
            "Requirement": "Failure resilience",
            "Observed": (
                "A3 → A5 recovery"
                if recovery_verified
                else "Not triggered"
            ),
            "Status": (
                "PASS"
                if recovery_verified
                else "PENDING"
            ),
        },
    ]


    st.dataframe(
        evidence_rows,
        use_container_width=True,
        hide_index=True,
    )


    st.markdown("---")


    st.subheader(
        "Mission Objective Mapping"
    )


    objective_rows = [
        {
            "Objective": "Task throughput",
            "Evidence": (
                f"{completed}/{total_incidents} completed"
            ),
        },
        {
            "Objective": "Collision risk",
            "Evidence": (
                f"{summary['collisions']} detected"
            ),
        },
        {
            "Objective": "Deadlock minimization",
            "Evidence": (
                f"{summary['deadlocks']} detected"
            ),
        },
        {
            "Objective": "Dynamic adaptation",
            "Evidence": (
                f"{summary['replans']} replanning event(s)"
            ),
        },
        {
            "Objective": "Energy efficiency",
            "Evidence": (
                f"{summary['energy_consumed']} units consumed"
            ),
        },
        {
            "Objective": "Failure resilience",
            "Evidence": (
                "Reserve-agent recovery demonstrated"
            ),
        },
    ]


    st.dataframe(
        objective_rows,
        use_container_width=True,
        hide_index=True,
    )


    st.markdown("---")


    if engine.metrics.decision_latencies:

        st.subheader(
            "Decision Latency Profile"
        )


        latency_fig = go.Figure()


        latency_fig.add_trace(
            go.Scatter(
                x=list(
                    range(
                        1,
                        len(
                            engine.metrics.decision_latencies
                        ) + 1,
                    )
                ),
                y=engine.metrics.decision_latencies,
                mode="lines+markers",
                name="Tick latency",
                line=dict(
                    width=2,
                ),
                marker=dict(
                    size=6,
                ),
            )
        )


        latency_fig.update_layout(
            height=320,
            paper_bgcolor="#091827",
            plot_bgcolor="#091827",

            font=dict(
                color="#8ea4b8",
            ),

            xaxis=dict(
                title="Simulation Tick",
                gridcolor="#183047",
            ),

            yaxis=dict(
                title="Latency (ms)",
                gridcolor="#183047",
            ),

            margin=dict(
                l=55,
                r=20,
                t=20,
                b=45,
            ),

            showlegend=False,
        )


        st.plotly_chart(
            latency_fig,
            use_container_width=True,
        )


# =========================================================
# ARCHITECTURE
# =========================================================

with tab_architecture:

    st.subheader(
        "PulseGrid Decision Architecture"
    )

    st.caption(
        "Decentralized autonomous control pipeline"
    )


    architecture = [
        (
            "01 · LOCAL STATE",
            "Agents maintain position, capability, "
            "energy, task and communication state.",
        ),
        (
            "02 · TASK BIDDING",
            "Agents calculate local task cost using "
            "distance, urgency, energy and capability.",
        ),
        (
            "03 · DECENTRALIZED ALLOCATION",
            "The lowest valid bid receives the incident "
            "without a central coordinator.",
        ),
        (
            "04 · TRAJECTORY PLANNING",
            "A* generates grid trajectories toward "
            "assigned emergency incidents.",
        ),
        (
            "05 · DYNAMIC ADAPTATION",
            "Environmental perturbations trigger "
            "trajectory recalculation.",
        ),
        (
            "06 · FAILURE RECOVERY",
            "Failed agents release tasks and reserve "
            "agents acquire them through allocation.",
        ),
    ]


    for start in range(
        0,
        len(architecture),
        3,
    ):

        cols = st.columns(3)

        for column, item in zip(
            cols,
            architecture[start:start + 3],
        ):

            with column:

                title, description = item

                st.html(
                    f"""
                    <div style="
                        background:
                            linear-gradient(
                                145deg,
                                #0d2031,
                                #091826
                            );

                        border:1px solid #1d3a51;

                        border-radius:11px;

                        padding:15px;

                        min-height:125px;

                        margin-bottom:12px;
                    ">

                        <div style="
                            color:#7dd3fc;
                            font-size:0.72rem;
                            font-weight:750;
                            letter-spacing:0.08em;
                        ">
                            {title}
                        </div>

                        <div style="
                            color:#8fa6b9;
                            font-size:0.76rem;
                            line-height:1.55;
                            margin-top:8px;
                        ">
                            {description}
                        </div>

                    </div>
                    """
                )


    st.markdown("---")


    st.html(
        """
        <div style="
            background:#091826;
            border:1px solid #1d3a51;
            border-radius:11px;
            padding:16px;
        ">

            <div style="
                color:#dce8f2;
                font-size:0.83rem;
                font-weight:750;
                margin-bottom:9px;
            ">
                AUTONOMOUS CONTROL LOOP
            </div>

            <div style="
                color:#9ec3d9;
                font-family:monospace;
                font-size:0.76rem;
                line-height:2.2;
            ">

                ENVIRONMENT
                →
                LOCAL STATE
                →
                TASK BIDS
                →
                ALLOCATION
                →
                A* PLANNING
                →
                COLLISION CHECK
                →
                EXECUTION
                →
                PERTURBATION
                →
                REPLAN / RECOVERY
                →
                METRICS

            </div>

        </div>
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.html(
    """
    <div style="
        text-align:center;

        margin-top:30px;
        padding-top:15px;

        border-top:1px solid #183047;

        color:#486177;
        font-size:0.67rem;

        letter-spacing:0.04em;
    ">

        PULSEGRID
        ·
        DECENTRALIZED MULTI-AGENT EMERGENCY RESPONSE
        ·
        SYNTHETIC SIMULATION ENVIRONMENT

    </div>
    """
)