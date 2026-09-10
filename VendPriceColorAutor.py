import streamlit as st
import math


# --------------------------------
# PAGE SETUP
# --------------------------------

st.set_page_config(
    page_title="SoPalm Price Generator",
    page_icon="🧮",
    layout="centered"
)


# --------------------------------
# MIAMI VICE STYLE
# --------------------------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(
                circle at top left,
                #103c5c 0%,
                #071b35 38%,
                #08091f 72%,
                #030611 100%
            );

        color: #f7f4ff;
    }


    /* --------------------------------
       MAIN SOPALM TITLE
       Cyan → Purple → Hot Pink
       -------------------------------- */

    h1 {
        background: linear-gradient(
            90deg,
            #5cffff 0%,
            #29dfff 25%,
            #8d8cff 50%,
            #e65cff 72%,
            #ff4fb8 100%
        );

        -webkit-background-clip: text;
        background-clip: text;

        -webkit-text-fill-color: transparent;

        font-weight: 800;

        filter: drop-shadow(
            0 0 5px rgba(41, 223, 255, 0.35)
        );

        letter-spacing: 0.3px;
    }


    /* Section titles */
    h2, h3 {
        color: #35eaff !important;
        font-weight: 800 !important;

        text-shadow:
            0 0 8px rgba(53, 234, 255, 0.25);
    }


    /* --------------------------------
       INPUT BOXES
       -------------------------------- */

    div[data-baseweb="input"] {
        background-color: #071a30;
        border: 1px solid #20dfff;
        border-radius: 12px;
        box-shadow: 0 0 8px rgba(32, 223, 255, 0.10);
    }


    div[data-baseweb="input"] input {
        color: #ffffff;
    }


    /* Input labels */
    label {
        color: #e2faff !important;
        font-weight: 500 !important;
    }


    /* --------------------------------
       YES / NO BUTTONS
       -------------------------------- */

    div[role="radiogroup"] label {

        background:
            rgba(
                8,
                24,
                48,
                0.96
            );

        border: 1px solid #20dfff;

        border-radius: 12px;

        padding: 10px 18px;

        margin-right: 12px;
    }


    /* Darker Yes / No wording */
    div[role="radiogroup"] label p {

        color: #8bb8c8 !important;

        font-weight: 600 !important;
    }


    /* Radio selection color */
    div[role="radiogroup"] input {
        accent-color: #ff3fae;
    }


    /* --------------------------------
       METRIC CARDS
       -------------------------------- */

    div[data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                rgba(9, 31, 55, 0.97),
                rgba(17, 10, 43, 0.97)
            );

        border: 1px solid #176f91;

        border-radius: 15px;

        padding: 12px 16px;

        box-shadow:
            0 0 14px
            rgba(32, 223, 255, 0.08);
    }


    /* Metric labels */
    div[data-testid="stMetricLabel"] {

        color: #f3ddeb !important;
    }


    /* Metric numbers */
    div[data-testid="stMetricValue"] {

        color: #35eaff !important;

        font-weight: 800;
    }


    /* --------------------------------
       DIVIDERS
       -------------------------------- */

    hr {

        border-color: #7a3db8 !important;

        opacity: 0.65;
    }


    /* --------------------------------
       PAGE SPACING
       -------------------------------- */

    .block-container {

        padding-top: 2rem;

        padding-bottom: 3rem;
    }


    /* Normal paragraph text */
    p {

        color: #f5edf4;
    }


    /* Miami Vice pink highlights */
    strong {

        color: #ff4fb8;
    }


    </style>
    """,

    unsafe_allow_html=True
)


# --------------------------------
# FUNCTIONS
# --------------------------------

def round_up_to_increment(
    price,
    increment
):

    return (
        math.ceil(
            price / increment
        )
        * increment
    )


def calculate_profit(
    case_cost,
    quantity,
    selling_price
):

    cost_per_item = (
        case_cost / quantity
    )


    profit_per_item = (
        selling_price
        - cost_per_item
    )


    revenue_per_case = (
        selling_price
        * quantity
    )


    profit_per_case = (
        revenue_per_case
        - case_cost
    )


    gross_margin = (
        profit_per_item
        / selling_price
    ) * 100


    return {

        "cost_per_item":
            cost_per_item,

        "profit_per_item":
            profit_per_item,

        "revenue_per_case":
            revenue_per_case,

        "profit_per_case":
            profit_per_case,

        "gross_margin":
            gross_margin
    }


# --------------------------------
# TITLE
# --------------------------------

st.title(
    "SoPalm Price Generator"
)


# --------------------------------
# INPUTS
# --------------------------------

st.subheader(
    "COST & PRICE INPUTS"
)


case_cost = st.number_input(

    "Case / Pack Cost ($)",

    min_value=0.01,

    value=None,

    step=0.01,

    placeholder="Enter case cost"
)


quantity = st.number_input(

    "Quantity (ct)",

    min_value=1,

    value=None,

    step=1,

    placeholder="Enter quantity"
)


# --------------------------------
# MARKUP MULTIPLIER
# --------------------------------

multiplier = st.number_input(

    "Markup Multiplier",

    min_value=1.0,

    value=None,

    step=0.01,

    placeholder="Enter multiplier (e.g., 2.00 = 2.00 x cost)"
)


# --------------------------------
# ONLY CALCULATE WHEN
# ALL INPUTS ARE ENTERED
# --------------------------------

if (
    case_cost is not None
    and quantity is not None
    and multiplier is not None
):


    # --------------------------------
    # EXACT PRICE
    # --------------------------------

    cost_per_item = (
        case_cost
        / quantity
    )


    exact_price = (
        cost_per_item
        * multiplier
    )


    exact_price = round(
        exact_price,
        2
    )


    # --------------------------------
    # NEXT QUARTER-DOLLAR PRICE
    # --------------------------------

    suggested_price = (
        round_up_to_increment(
            exact_price,
            0.25
        )
    )


    suggested_price = round(
        suggested_price,
        2
    )


    # --------------------------------
    # EXACT MARKUP PRICE
    # --------------------------------

    st.write("")


    st.metric(
        "Exact Markup Price",
        f"${exact_price:.2f}"
    )


    # --------------------------------
    # ROUNDING QUESTION
    # --------------------------------

    if not math.isclose(
        exact_price,
        suggested_price,
        abs_tol=0.001
    ):

        st.markdown(
            f'<p style="margin-top:18px; margin-bottom:14px; font-size:17px;">Round <strong>${exact_price:.2f}</strong> up to the next quarter-dollar price of <strong>${suggested_price:.2f}</strong>?</p>',
            unsafe_allow_html=True
        )


        rounding_choice = st.radio(

            "Choose Selling Price",

            options=[
                "Yes",
                "No"
            ],

            format_func=lambda x:
                (
                    f"Yes — Use "
                    f"${suggested_price:.2f}"
                )

                if x == "Yes"

                else

                (
                    f"No — Keep "
                    f"${exact_price:.2f}"
                ),

            horizontal=True,

            label_visibility="collapsed"
        )


        if rounding_choice == "Yes":

            selling_price = (
                suggested_price
            )


        else:

            selling_price = (
                exact_price
            )


    else:

        selling_price = (
            exact_price
        )


        st.caption(
            "This price is already on a "
            "quarter-dollar increment."
        )


    # --------------------------------
    # CALCULATE PROFIT
    # --------------------------------

    results = calculate_profit(

        case_cost,

        quantity,

        selling_price
    )


    # --------------------------------
    # SELLING PRICE
    #
    # NO RESULTS TITLE
    # --------------------------------

    st.write("")


    selling_col, empty_col = st.columns(
        [1, 2]
    )


    with selling_col:

        st.metric(
            "Selling Price",
            f"${selling_price:.2f}"
        )


    # --------------------------------
    # PROFIT SUMMARY
    # --------------------------------

    st.divider()


    st.subheader(
        "PROFIT SUMMARY"
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Cost / Item",
            f"${results['cost_per_item']:.2f}"
        )


        st.metric(
            "Profit / Item",
            f"${results['profit_per_item']:.2f}"
        )


        st.metric(
            "Profit / Case",
            f"${results['profit_per_case']:.2f}"
        )


    with col2:

        st.metric(
            "Sell Price",
            f"${selling_price:.2f}"
        )


        st.metric(
            "Revenue / Case",
            f"${results['revenue_per_case']:.2f}"
        )


        st.metric(
            "Gross Margin",
            f"{results['gross_margin']:.1f}%"
        )


    # --------------------------------
    # SOPALM RECOMMENDATION
    # HIDDEN FOR NOW
    #
    # REMOVE THE # SYMBOLS IF
    # YOU WANT TO RESTORE IT LATER
    # --------------------------------

    # st.divider()

    # st.markdown(
    #     f"""
    #     ### 🧮 SoPalm Recommendation
    #
    #     Sell each item for
    #     **${selling_price:.2f}**.
    #
    #     Gross profit per item:
    #     **${results['profit_per_item']:.2f}**
    #
    #     Gross profit per case:
    #     **${results['profit_per_case']:.2f}**
    #
    #     Gross margin:
    #     **{results['gross_margin']:.1f}%**
    #     """
    # )
