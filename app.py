import streamlit as st
import subprocess
import tempfile
import os

st.set_page_config(
    page_title="AI-IaC Configuration Validator",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 AI-Based IaC Configuration Validation")
st.write("CVS + Checkov + AI-Assisted Change Control")

st.divider()

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Module",
    [
        "🏠 Dashboard",
        "📄 IaC Configuration",
        "🔍 Checkov Validation",
        "🤖 AI Explanation",
        "📚 CVS History"
    ]
)

if "checkov_output" not in st.session_state:
    st.session_state.checkov_output = ""

if "uploaded_code" not in st.session_state:
    st.session_state.uploaded_code = ""


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

if page == "🏠 Dashboard":

    st.header("📊 Project Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Validation Tool", "Checkov")

    with col2:
        st.metric("Configuration Control", "CVS")

    with col3:
        st.metric("AI Assistance", "Enabled")

    st.divider()

    st.subheader("Project Workflow")

    st.info(
        "IaC Configuration → Checkov Validation → "
        "AI Explanation → Correction → Re-validation → CVS History"
    )

    st.markdown("""
    ### Main Purpose

    This system validates Infrastructure as Code configurations,
    identifies security or policy violations, explains detected
    problems in simple language, and maintains configuration
    change history.
    """)


# ---------------------------------------------------------
# IAC CONFIGURATION
# ---------------------------------------------------------

elif page == "📄 IaC Configuration":

    st.header("📄 Infrastructure as Code Configuration")

    st.write(
        "Upload any Terraform (.tf) file that you want to validate."
    )

    uploaded_file = st.file_uploader(
        "Upload Terraform Configuration",
        type=["tf"]
    )

    if uploaded_file is not None:

        file_content = uploaded_file.read().decode("utf-8")

        st.session_state.uploaded_code = file_content

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )

        st.subheader("Configuration Preview")

        st.code(
            file_content,
            language="hcl"
        )

    else:

        st.info(
            "Please upload a Terraform (.tf) file."
        )


# ---------------------------------------------------------
# CHECKOV VALIDATION
# ---------------------------------------------------------

elif page == "🔍 Checkov Validation":

    st.header("🔍 Checkov Validation")

    if not st.session_state.uploaded_code:

        st.warning(
            "Please upload a Terraform (.tf) file first "
            "from the IaC Configuration page."
        )

    else:

        st.subheader("Configuration Being Tested")

        st.code(
            st.session_state.uploaded_code,
            language="hcl"
        )

        if st.button(
            "🔍 Run Checkov Validation",
            use_container_width=True
        ):

            with tempfile.TemporaryDirectory() as temp_dir:

                tf_file = os.path.join(
                    temp_dir,
                    "configuration.tf"
                )

                with open(
                    tf_file,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(
                        st.session_state.uploaded_code
                    )

                try:

                    result = subprocess.run(
                        [
                            "checkov",
                            "-f",
                            tf_file,
                            "--output",
                            "cli"
                        ],
                        capture_output=True,
                        text=True,
                        timeout=120
                    )

                    output = (
                        result.stdout +
                        "\n" +
                        result.stderr
                    )

                    st.session_state.checkov_output = output

                    st.subheader("Checkov Result")

                    if result.returncode == 0:

                        st.success(
                            "✅ Checkov validation completed."
                        )

                    else:

                        st.error(
                            "❌ Checkov detected one or more "
                            "issues or the validation returned "
                            "a non-zero status."
                        )

                    st.code(
                        output,
                        language="text"
                    )

                except FileNotFoundError:

                    st.error(
                        "Checkov is not installed or is not "
                        "available in the deployment environment."
                    )

                except subprocess.TimeoutExpired:

                    st.error(
                        "Checkov validation timed out."
                    )


# ---------------------------------------------------------
# AI EXPLANATION
# ---------------------------------------------------------

elif page == "🤖 AI Explanation":

    st.header("🤖 AI-Assisted Explanation")

    if not st.session_state.checkov_output:

        st.warning(
            "Run Checkov validation first."
        )

    else:

        st.subheader("Checkov Technical Result")

        st.code(
            st.session_state.checkov_output,
            language="text"
        )

        st.subheader("Simple Explanation")

        output_lower = (
            st.session_state.checkov_output.lower()
        )

        if (
            "0.0.0.0/0" in st.session_state.uploaded_code
            and "22" in st.session_state.uploaded_code
        ):

            st.info("""
The configuration allows SSH access from all IPv4
addresses.

Port 22 is commonly used for SSH.

Recommended action:
Restrict SSH access to a trusted IP address or
internal network instead of allowing access from
0.0.0.0/0.
""")

        elif "failed" in output_lower:

            st.info("""
Checkov has reported one or more failed checks.

Review the failed rule IDs and configuration
details shown above. Correct the configuration
and run the validation again.
""")

        else:

            st.success("""
No obvious failed Checkov checks were identified
in the displayed result.

Always review the complete Checkov output before
accepting the configuration.
""")


# ---------------------------------------------------------
# CVS HISTORY
# ---------------------------------------------------------

elif page == "📚 CVS History":

    st.header("📚 CVS Configuration History")

    st.write(
        "This section represents the configuration revision "
        "history maintained by CVS."
    )

    history = [
        {
            "Revision": "1.1",
            "Change": "Initial IaC configuration",
            "Validation": "Failed",
            "Status": "❌ Requires correction"
        },
        {
            "Revision": "1.2",
            "Change": "Restricted SSH access",
            "Validation": "Re-validated",
            "Status": "✅ Corrected"
        }
    ]

    st.table(history)

    st.info(
        "In the complete implementation, CVS maintains the "
        "actual revision history of the IaC configuration."
    )
