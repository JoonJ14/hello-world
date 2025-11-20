import React from 'react';
import { Link, useLocation } from 'react-router-dom';

export default function Layout({ children }) {
    const location = useLocation();

    return (
        <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
            <header style={{
                background: 'var(--color-surface)',
                borderBottom: '1px solid var(--color-border)',
                padding: 'var(--space-sm) 0'
            }}>
                <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Link to="/" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <div style={{
                            width: '32px',
                            height: '32px',
                            background: 'var(--color-primary)',
                            borderRadius: '8px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            color: 'white',
                            fontWeight: 'bold'
                        }}>
                            H
                        </div>
                        <span style={{ fontSize: '1.25rem', fontWeight: '700', color: 'var(--color-text-main)' }}>
                            HealthGuard
                        </span>
                    </Link>

                    <nav>
                        {location.pathname !== '/' && location.pathname !== '/profile-setup' && (
                            <Link to="/profile-setup" className="btn btn-outline" style={{ fontSize: '0.875rem', padding: '0.5rem 1rem' }}>
                                Update Insurance
                            </Link>
                        )}
                    </nav>
                </div>
            </header>

            <main style={{ flex: 1, padding: 'var(--space-lg) 0' }}>
                <div className="container">
                    {children}
                </div>
            </main>

            <footer style={{
                textAlign: 'center',
                padding: 'var(--space-lg) 0',
                color: 'var(--color-text-muted)',
                fontSize: '0.875rem'
            }}>
                <p>© {new Date().getFullYear()} HealthGuard. Your health, transparently priced.</p>
            </footer>
        </div>
    );
}
