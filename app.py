import streamlit as st
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'ai'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'blockchain'))

from risk_engine import calculate_combined_risk
from blockchain_verification import HederaVerifier, MockHederaVerifier

st.set_page_config(
    page_title="WealthGuard AI", 
    page_icon=" ", 
    layout="wide"
)

st.title("💼 WealthGuard AI - Secure Digital Wealth Companion")
st.markdown("### AI-Powered Portfolio Management with Blockchain Security")

if 'verifier' not in st.session_state:
    st.session_state.verifier = MockHederaVerifier()  # Start with mock verifier

st.sidebar.header("Quick Setup")
if st.sidebar.button("Initialize Hedera Blockchain"):
    try:
        from blockchain.hedera_urgent_setup import emergency_hedera_setup
        client, private_key, account_id = emergency_hedera_setup()
        
        
        verifier = HederaVerifier()
        verifier.setup_credentials(str(private_key), str(account_id))
        st.session_state.verifier = verifier
        
        st.sidebar.success(" Hedera Blockchain Connected!")
    except Exception as e:
        st.sidebar.error(f" Hedera setup failed: {e}")


col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(" Portfolio Analysis")
    
    # Portfolio selection
    assets = st.multiselect(
        "Select Assets for Your Portfolio",
        ["BTC", "ETH", "AAPL", "TSLA", "GOOGL", "MSFT", "BOND", "GOLD"],
        default=["BTC", "AAPL", "BOND"],
        help="Choose assets to analyze risk and get AI recommendations"
    )
    
    if st.button("Analyze Portfolio Risk", type="primary"):
        if not assets:
            st.error("Please select at least one asset.")
        else:
            # AI Risk Analysis
            with st.spinner(" AI analyzing portfolio risks..."):
                risk_result = calculate_combined_risk(assets)
            
            # Display results
            st.success("Analysis Complete!")
            
            # Metrics
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Overall Risk", f"{risk_result['combined_score']}/10")
            with c2:
                st.metric("Financial Risk", f"{risk_result['financial_risk']}/10")
            with c3:
                st.metric("Security Risk", f"{risk_result['security_risk']}/10")
            
            # Recommendation
            st.info(f"**Recommendation:** {risk_result['recommendation']}")
            
            # Blockchain Verification Section
            st.subheader(" Blockchain Verification")
            st.write("Verify this decision on Hedera blockchain for immutable record keeping")
            
            if st.button("Verify on Blockchain", type="secondary"):
                with st.spinner("Creating blockchain transaction..."):
                    blockchain_result = st.session_state.verifier.verify_portfolio_decision(
                        assets, 
                        risk_result['combined_score'],
                        risk_result['recommendation']
                    )
                
                if blockchain_result['success']:
                    st.success("✅ Successfully verified on Hedera Blockchain!")
                    
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(f"**Transaction ID:** {blockchain_result['transaction_id']}")
                        st.write(f"**Status:** {blockchain_result['status']}")
                    with c2:
                        st.write(f"**Memo:** {blockchain_result['memo']}")
                        if 'explorer_url' in blockchain_result:
                            st.markdown(f"**Explorer:** [View on HashScan]({blockchain_result['explorer_url']})")
                    
                    if 'note' in blockchain_result:
                        st.warning(blockchain_result['note'])
                else:
                    st.error(f"❌ Blockchain verification failed: {blockchain_result['error']}")

with col2:
    st.subheader("🧭 How It Works")
    st.markdown("""
**1. Select Assets**  
Choose from crypto, stocks, or bonds.

**2. AI Risk Analysis**  
- Financial volatility scoring  
- Protocol security assessment  
- Combined risk calculation

**3. Blockchain Verification**  
- Immutable transaction record  
- Hedera Hashgraph technology  
- Transparent audit trail
""")
    
    st.subheader(" Competition Features")
    st.markdown("""
**AI/ML** - Risk scoring engine  
**Blockchain** - Hedera verification  
**Cybersecurity** - Protocol analysis  
**FinTech** - Portfolio management
""")

st.markdown("---")
st.markdown("Built for **AIxCYBER2025 Hackathon** | Secure Digital Wealth Companion")
