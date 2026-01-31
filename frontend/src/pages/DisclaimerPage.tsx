import { Link } from "react-router-dom";
import styles from "./DisclaimerPage.module.css";

function DisclaimerPage() {
    return (
        <div className={styles.page}>
            <header className={styles.header}>
                <h1 className={styles.title}>Disclaimer</h1>
                <p className={styles.subtitle}>
                    Important information about using ASX Trading Lab
                </p>
            </header>

            <section className={styles.content}>
                <div className={styles.warningBanner}>
                    <strong>Educational and Research Purpose Only</strong>
                    <p>
                        ASX Trading Lab is designed as a decision-support and research tool. 
                        It is not intended to provide, and should not be construed as, 
                        financial advice, investment recommendations, or trading signals 
                        that you should follow without independent analysis.
                    </p>
                </div>

                <article className={styles.section}>
                    <h2>Not Financial Advice</h2>
                    <p>
                        The information provided by ASX Trading Lab, including but not limited to 
                        signals, analytics, backtests, and paper trading results:
                    </p>
                    <ul>
                        <li>Does not constitute financial, investment, legal, or tax advice</li>
                        <li>Should not be the sole basis for any investment decision</li>
                        <li>Does not take into account your personal financial situation, objectives, or risk tolerance</li>
                        <li>Is provided for educational and research purposes only</li>
                    </ul>
                    <p>
                        <strong>Always consult with a qualified financial advisor, licensed broker, 
                        or other appropriate professional before making any investment decisions.</strong>
                    </p>
                </article>

                <article className={styles.section}>
                    <h2>Data Accuracy and Timeliness</h2>
                    <p>
                        While we strive to provide accurate and timely information, you should be aware that:
                    </p>
                    <ul>
                        <li>Price data may be delayed by 15 minutes or more from real-time market data</li>
                        <li>Data sourced from third-party providers (such as Yahoo Finance) may contain errors or omissions</li>
                        <li>Historical data may be incomplete or subject to corporate action adjustments</li>
                        <li>Signal calculations are based on historical patterns and may not reflect current market conditions</li>
                        <li>Technical issues may cause data gaps or incorrect values</li>
                    </ul>
                    <p>
                        <strong>Do not rely solely on the data provided here. Always verify 
                        information through official sources before making trading decisions.</strong>
                    </p>
                </article>

                <article className={styles.section}>
                    <h2>Signal Interpretation Guidelines</h2>
                    <p>
                        The signals and analytics provided by this platform:
                    </p>
                    <ul>
                        <li><strong>May indicate</strong> potential price movements, but do not guarantee outcomes</li>
                        <li><strong>Suggest</strong> areas of interest based on technical analysis, not certainties</li>
                        <li><strong>Highlight</strong> statistical patterns that have occurred historically</li>
                        <li><strong>Should be considered</strong> as one input among many in your research process</li>
                    </ul>
                    <p>
                        Avoid interpreting any signal as a recommendation to buy, sell, or hold any security. 
                        Past performance, whether in backtests or historical signals, does not guarantee future results.
                    </p>
                </article>

                <article className={styles.section}>
                    <h2>Backtesting and Paper Trading Limitations</h2>
                    <p>
                        Backtesting and paper trading results shown on this platform:
                    </p>
                    <ul>
                        <li>Are hypothetical and do not represent actual trading</li>
                        <li>Do not account for slippage, market impact, or liquidity constraints</li>
                        <li>May not reflect the actual costs of trading including brokerage fees, taxes, and spreads</li>
                        <li>Are based on historical data and may not be indicative of future performance</li>
                        <li>May be subject to survivorship bias and look-ahead bias</li>
                    </ul>
                </article>

                <article className={styles.section}>
                    <h2>Risk Warning</h2>
                    <div className={styles.riskWarning}>
                        <p>
                            <strong>Trading and investing in securities involves substantial risk of loss 
                            and is not suitable for all investors.</strong>
                        </p>
                        <p>
                            You could lose some or all of your invested capital. Do not invest money you 
                            cannot afford to lose. The value of investments can go down as well as up.
                        </p>
                        <p>
                            If you are unsure about investing, seek independent professional financial advice.
                        </p>
                    </div>
                </article>

                <article className={styles.section}>
                    <h2>No Warranty</h2>
                    <p>
                        ASX Trading Lab is provided &quot;as is&quot; without warranty of any kind, express or implied. 
                        We do not warrant that:
                    </p>
                    <ul>
                        <li>The service will be uninterrupted or error-free</li>
                        <li>The data or results will be accurate, complete, or reliable</li>
                        <li>Any signals or strategies will be profitable</li>
                        <li>The platform will meet your specific requirements</li>
                    </ul>
                </article>

                <article className={styles.section}>
                    <h2>Limitation of Liability</h2>
                    <p>
                        To the maximum extent permitted by applicable law, ASX Trading Lab and its creators 
                        shall not be liable for any direct, indirect, incidental, special, consequential, 
                        or punitive damages arising from:
                    </p>
                    <ul>
                        <li>Your use or inability to use the platform</li>
                        <li>Any errors or omissions in the data or content</li>
                        <li>Trading decisions made based on information provided</li>
                        <li>Any investment losses or financial damages</li>
                    </ul>
                </article>

                <article className={styles.section}>
                    <h2>Your Responsibilities</h2>
                    <p>
                        By using ASX Trading Lab, you acknowledge and agree that:
                    </p>
                    <ul>
                        <li>You are solely responsible for your own investment decisions</li>
                        <li>You will conduct your own due diligence before trading</li>
                        <li>You understand and accept the risks associated with investing</li>
                        <li>You will not hold us liable for any losses incurred</li>
                        <li>You are using this platform for educational and research purposes</li>
                    </ul>
                </article>

                <div className={styles.footer}>
                    <p>
                        By continuing to use ASX Trading Lab, you acknowledge that you have read, 
                        understood, and agree to the terms outlined in this disclaimer.
                    </p>
                    <Link to="/" className={styles.backLink}>
                        ← Return to Dashboard
                    </Link>
                </div>
            </section>
        </div>
    );
}

export default DisclaimerPage;
