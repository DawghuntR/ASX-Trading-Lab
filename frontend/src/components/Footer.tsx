import styles from "./Footer.module.css";

function Footer() {
    const currentYear = new Date().getFullYear();

    return (
        <footer className={styles.footer}>
            <div className={styles.container}>
                <p className={styles.disclaimer}>
                    For informational purposes only. Not financial advice.
                </p>
                <p className={styles.copyright}>
                    © {currentYear} ASX Trading Lab
                </p>
            </div>
        </footer>
    );
}

export default Footer;
