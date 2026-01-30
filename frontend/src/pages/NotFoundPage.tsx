import { Link } from "react-router-dom";
import styles from "./NotFoundPage.module.css";

function NotFoundPage() {
    return (
        <div className={styles.page}>
            <div className={styles.content}>
                <h1 className={styles.code}>404</h1>
                <h2 className={styles.title}>Page Not Found</h2>
                <p className={styles.message}>
                    The page you&apos;re looking for doesn&apos;t exist or has
                    been moved.
                </p>
                <Link
                    to="/"
                    className={styles.link}>
                    Return to Dashboard
                </Link>
            </div>
        </div>
    );
}

export default NotFoundPage;
