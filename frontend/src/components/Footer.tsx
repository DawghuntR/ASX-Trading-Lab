import { Link } from "react-router-dom";
import styles from "./Footer.module.css";

function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className={styles.footer}>
            <div className={styles.container}>
                <div className={styles.disclaimer}>
                    <p className={styles.disclaimerText}>
                        <strong>Important:</strong> This platform is for educational and research purposes only. 
                        It does not constitute financial advice. Data may be delayed, incomplete, or inaccurate. 
                        Always consult a qualified financial advisor before making investment decisions.
                    </p>
                    <Link to="/disclaimer" className={styles.disclaimerLink}>
                        Read full disclaimer →
                    </Link>
                </div>
                <p className={styles.copyright}>
                    © {currentYear} ASX Trading Lab
                </p>
            </div>
        </footer>
    );
}

export default Footer;
