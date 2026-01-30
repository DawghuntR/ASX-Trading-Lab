import { Link, NavLink } from "react-router-dom";
import styles from "./Header.module.css";

function Header() {
    return (
        <header className={styles.header}>
            <div className={styles.container}>
                <Link
                    to="/"
                    className={styles.logo}>
                    <span className={styles.logoIcon}>📈</span>
                    <span className={styles.logoText}>ASX Trading Lab</span>
                </Link>
                <nav className={styles.nav}>
                    <NavLink
                        to="/"
                        className={({ isActive }) =>
                            isActive ? styles.navLinkActive : styles.navLink
                        }
                        end>
                        Dashboard
                    </NavLink>
                    <NavLink
                        to="/signals"
                        className={({ isActive }) =>
                            isActive ? styles.navLinkActive : styles.navLink
                        }>
                        Signals
                    </NavLink>
                    <NavLink
                        to="/backtests"
                        className={({ isActive }) =>
                            isActive ? styles.navLinkActive : styles.navLink
                        }>
                        Backtests
                    </NavLink>
                    <NavLink
                        to="/portfolio"
                        className={({ isActive }) =>
                            isActive ? styles.navLinkActive : styles.navLink
                        }>
                        Portfolio
                    </NavLink>
                </nav>
            </div>
        </header>
    );
}

export default Header;
