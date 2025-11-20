import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

export default function SymptomChecker() {
    const [symptoms, setSymptoms] = useState('');
    const [results, setResults] = useState(null);
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        const saved = localStorage.getItem('healthProfile');
        if (saved) {
            setProfile(JSON.parse(saved));
        }
    }, []);

    // Mock Database of Conditions
    const CONDITIONS = [
        { keywords: ['headache', 'head', 'pain'], name: 'Migraine', baseCost: 300, severity: 'Moderate' },
        { keywords: ['fever', 'cough', 'cold', 'sneeze'], name: 'Viral Upper Respiratory Infection', baseCost: 150, severity: 'Low' },
        { keywords: ['chest', 'heart', 'breath'], name: 'Cardiology Consultation (Potential)', baseCost: 2500, severity: 'High' },
        { keywords: ['stomach', 'belly', 'pain', 'nausea'], name: 'Gastritis', baseCost: 600, severity: 'Moderate' },
        { keywords: ['back', 'spine', 'ache'], name: 'Lumbar Strain', baseCost: 400, severity: 'Low' },
    ];

    const calculateCost = (baseCost) => {
        if (!profile) return { total: baseCost, user: baseCost, insurance: 0 };

        let multiplier = 1.0;

        // Age Factor: +2% per year over 20
        if (profile.age > 20) {
            multiplier += (profile.age - 20) * 0.02;
        }

        // Tobacco Factor: +50%
        if (profile.tobacco) {
            multiplier += 0.5;
        }

        // Region Factor
        const regionFactors = { 'NY': 1.2, 'CA': 1.15, 'IL': 1.05, 'TX': 0.95, 'FL': 1.0 };
        multiplier *= (regionFactors[profile.state] || 1.0);

        const totalEstimatedCost = baseCost * multiplier;

        // Insurance Logic
        // Simplified: User pays Copay + Deductible (if not met) + Coinsurance
        // We'll assume Deductible is NOT met for this scenario to show worst-case "new" cost

        // 1. Copay is flat
        let userCost = Number(profile.copay);

        // 2. Remaining after copay
        let remaining = Math.max(0, totalEstimatedCost - userCost);

        // 3. Deductible logic (assuming full deductible needs to be paid)
        let deductiblePayment = Math.min(remaining, Number(profile.deductible));
        userCost += deductiblePayment;
        remaining -= deductiblePayment;

        // 4. Coinsurance on the rest
        let coinsurancePayment = remaining * (Number(profile.coinsurance) / 100);
        userCost += coinsurancePayment;

        // Cap user cost at total cost (sanity check)
        userCost = Math.min(userCost, totalEstimatedCost);

        return {
            total: totalEstimatedCost,
            user: userCost,
            insurance: totalEstimatedCost - userCost
        };
    };

    const handleCheck = (e) => {
        e.preventDefault();
        setLoading(true);
        setResults(null);

        // Simulate API delay
        setTimeout(() => {
            const text = symptoms.toLowerCase();
            const matches = CONDITIONS.filter(c =>
                c.keywords.some(k => text.includes(k))
            );

            // Default if no matches
            if (matches.length === 0) {
                matches.push({ name: 'General Consultation', baseCost: 200, severity: 'Unknown' });
            }

            const calculatedResults = matches.map(condition => ({
                ...condition,
                costs: calculateCost(condition.baseCost)
            }));

            setResults(calculatedResults);
            setLoading(false);
        }, 1500);
    };

    if (!profile) {
        return (
            <div className="container" style={{ textAlign: 'center', padding: 'var(--space-xl) 0' }}>
                <h2>Profile Not Found</h2>
                <p>Please set up your insurance profile first.</p>
                <Link to="/" className="btn btn-primary" style={{ marginTop: 'var(--space-md)' }}>
                    Go to Setup
                </Link>
            </div>
        );
    }

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto' }}>
            <div style={{ textAlign: 'center', marginBottom: 'var(--space-lg)' }}>
                <h1 style={{ fontSize: '2.5rem', marginBottom: 'var(--space-xs)', color: 'var(--color-primary-dark)' }}>
                    Symptom Checker
                </h1>
                <p style={{ color: 'var(--color-text-muted)', fontSize: '1.125rem' }}>
                    Describe your symptoms to get estimated costs based on your <b>{profile.insuranceCompany} {profile.planName}</b> plan.
                </p>
            </div>

            <div className="card" style={{ marginBottom: 'var(--space-xl)' }}>
                <form onSubmit={handleCheck}>
                    <div className="input-group">
                        <label className="input-label">How are you feeling today?</label>
                        <textarea
                            className="input-field"
                            rows="4"
                            placeholder="e.g. I have a throbbing headache and sensitivity to light..."
                            value={symptoms}
                            onChange={(e) => setSymptoms(e.target.value)}
                            required
                        />
                    </div>
                    <div style={{ textAlign: 'right' }}>
                        <button type="submit" className="btn btn-primary" disabled={loading}>
                            {loading ? 'Analyzing...' : 'Check Symptoms & Prices'}
                        </button>
                    </div>
                </form>
            </div>

            {results && (
                <div style={{ animation: 'fadeIn 0.5s ease' }}>
                    <h2 style={{ marginBottom: 'var(--space-md)' }}>Potential Conditions & Costs</h2>
                    <div style={{ display: 'grid', gap: 'var(--space-md)' }}>
                        {results.map((item, index) => (
                            <div key={index} className="card" style={{ borderLeft: `6px solid var(--color-primary)` }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 'var(--space-md)' }}>
                                    <div>
                                        <h3 style={{ fontSize: '1.25rem', color: 'var(--color-text-main)' }}>{item.name}</h3>
                                        <span style={{
                                            display: 'inline-block',
                                            padding: '0.25rem 0.75rem',
                                            borderRadius: 'var(--radius-full)',
                                            fontSize: '0.75rem',
                                            fontWeight: '600',
                                            background: 'var(--color-surface-alt)',
                                            color: 'var(--color-text-muted)',
                                            marginTop: '0.5rem'
                                        }}>
                                            Severity: {item.severity}
                                        </span>
                                    </div>
                                    <div style={{ textAlign: 'right' }}>
                                        <div style={{ fontSize: '0.875rem', color: 'var(--color-text-muted)' }}>Estimated Total</div>
                                        <div style={{ fontSize: '1.5rem', fontWeight: '700' }}>
                                            ${item.costs.total.toFixed(0)}
                                        </div>
                                    </div>
                                </div>

                                {/* Cost Visualization */}
                                <div style={{ background: 'var(--color-surface-alt)', borderRadius: 'var(--radius-md)', padding: 'var(--space-md)' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', marginBottom: 'var(--space-xs)' }}>
                                        <div style={{ flex: 1, fontSize: '0.875rem', fontWeight: '600' }}>Your Cost</div>
                                        <div style={{ fontSize: '1.125rem', fontWeight: '700', color: 'var(--color-accent)' }}>
                                            ${item.costs.user.toFixed(0)}
                                        </div>
                                    </div>

                                    {/* Progress Bar */}
                                    <div style={{ height: '12px', background: '#e2e8f0', borderRadius: '6px', overflow: 'hidden', display: 'flex', marginBottom: 'var(--space-xs)' }}>
                                        <div style={{
                                            width: `${(item.costs.user / item.costs.total) * 100}%`,
                                            background: 'var(--color-accent)',
                                            transition: 'width 1s ease'
                                        }} />
                                        <div style={{
                                            width: `${(item.costs.insurance / item.costs.total) * 100}%`,
                                            background: 'var(--color-primary)',
                                            transition: 'width 1s ease'
                                        }} />
                                    </div>

                                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                                        <span>You Pay ({((item.costs.user / item.costs.total) * 100).toFixed(0)}%)</span>
                                        <span>Insurance Pays ({((item.costs.insurance / item.costs.total) * 100).toFixed(0)}%)</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
