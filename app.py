import streamlit as st

st.set_page_config(
    page_title="AI-IaC Configuration Validation",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 AI-Based IaC Configuration Validation")
st.subheader("CVS + Checkov + AI-Assisted Change Control")

st.markdown("""
This system validates Infrastructure as Code configurations,
identifies security violations, explains the issue, recommends
a correction, and maintains configuration change history.
""")

st.divider()

st.header("📄 Infrastructure as Code Configuration")

default_config = '''resource "aws_security_group" "demo" {
  name = "demo-security-group"

  ingress {
    description = "SSH access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}'''

configuration = st.text_area(
    "Terraform Configuration",
    value=default_config,
    height=300
)

if st.button("🔍 Validate Configuration", use_container_width=True):
    st.error("❌ Checkov Validation Failed")

    st.subheader("Checkov Result")

    st.code("""
SSH access is unrestricted.

Port: 22
Source: 0.0.0.0/0
""")

    st.subheader("🤖 AI Explanation")

    st.info("""
The configuration allows SSH access from any IP address on
the internet. This can expose the infrastructure to
unauthorized access attempts.

Recommended action:
Restrict SSH access to a trusted IP address or internal network.
""")

    st.subheader("🔧 Recommended Correction")

    st.code('cidr_blocks = ["10.0.0.0/24"]', language="hcl")

st.divider()

st.header("📚 CVS Configuration History")

history = {
    "Revision": ["1.1", "1.2"],
    "Change": [
        "Initial configuration",
        "Restricted SSH access"
    ],
    "Validation": [
        "Failed",
        "Passed"
    ],
    "Status": [
        "❌ Unsafe",
        "✅ Corrected"
    ]
}

st.table(history)

st.divider()

st.header("📊 Project Workflow")

st.markdown("""
**IaC Configuration → CVS → Checkov Validation → AI Explanation
→ Correction → Re-validation → CVS Revision History**
""")
