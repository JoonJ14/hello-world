import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

export default function InsuranceProfile() {
    const navigate = useNavigate();
    const location = useLocation();

    // Load initial state from location (upload), localStorage, or default
    const [formData, setFormData] = useState(() => {
        if (location.state?.extractedData) {
            return location.state.extractedData;
        }
        const saved = localStorage.getItem('healthProfile');
        return saved ? JSON.parse(saved) : {
            age: 30,
            gender: 'female',
            state: 'CA',
            tobacco: false,
            insuranceCompany: 'BlueCross',
            planName: 'Gold Standard',
            deductible: 1500,
            copay: 25,
            coinsurance: 20 // % user pays
        };
    });

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        localStorage.setItem('healthProfile', JSON.stringify(formData));
        navigate('/symptom-checker');
    };

    return (
        <div style={{ maxWidth: '600px', margin: '0 auto' }}>
            <div style={{ textAlign: 'center', marginBottom: 'var(--space-lg)' }}>
                <h1 style={{ fontSize: '2.5rem', marginBottom: 'var(--space-xs)', color: 'var(--color-primary-dark)' }}>
                    Your Health Profile
                </h1>
                <p style={{ color: 'var(--color-text-muted)', fontSize: '1.125rem' }}>
                    Tell us about yourself and your insurance to get accurate cost estimates.
                </p>
            </div>

            <form onSubmit={handleSubmit} className="card">
                <h2 style={{ marginBottom: 'var(--space-md)', borderBottom: '1px solid var(--color-border)', paddingBottom: 'var(--space-sm)' }}>
                    Demographics
                </h2>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 'var(--space-md)' }}>
                    <div className="input-group">
                        <label className="input-label">Age</label>
                        <input
                            type="number"
                            name="age"
                            value={formData.age}
                            onChange={handleChange}
                            className="input-field"
                            min="0"
                            max="120"
                            required
                        />
                    </div>

                    <div className="input-group">
                        <label className="input-label">Gender</label>
                        <select
                            name="gender"
                            value={formData.gender}
                            onChange={handleChange}
                            className="input-field"
                        >
                            <option value="female">Female</option>
                            <option value="male">Male</option>
                            <option value="other">Other</option>
                        </select>
                    </div>

                    <div className="input-group">
                        <label className="input-label">State</label>
                        <select
                            name="state"
                            value={formData.state}
                            onChange={handleChange}
                            className="input-field"
                        >
                            <option value="CA">California</option>
                            <option value="NY">New York</option>
                            <option value="TX">Texas</option>
                            <option value="FL">Florida</option>
                            <option value="IL">Illinois</option>
                            {/* Add more as needed */}
                        </select>
                    </div>
                </div>

                <div className="input-group" style={{ display: 'flex', alignItems: 'center', gap: 'var(--space-sm)' }}>
                    <input
                        type="checkbox"
                        id="tobacco"
                        name="tobacco"
                        checked={formData.tobacco}
                        onChange={handleChange}
                        style={{ width: '1.25rem', height: '1.25rem', accentColor: 'var(--color-primary)' }}
                    />
                    <label htmlFor="tobacco" className="input-label" style={{ marginBottom: 0 }}>
                        I am a tobacco user
                    </label>
                </div>

                <h2 style={{ margin: 'var(--space-lg) 0 var(--space-md)', borderBottom: '1px solid var(--color-border)', paddingBottom: 'var(--space-sm)' }}>
                    Insurance Details
                </h2>

                <div className="input-group">
                    <label className="input-label">Insurance Company</label>
                    <input
                        type="text"
                        name="insuranceCompany"
                        value={formData.insuranceCompany}
                        onChange={handleChange}
                        className="input-field"
                        placeholder="e.g. BlueCross, Aetna, UnitedHealthcare"
                        required
                    />
                </div>

                <div className="input-group">
                    <label className="input-label">Plan Name</label>
                    <input
                        type="text"
                        name="planName"
                        value={formData.planName}
                        onChange={handleChange}
                        className="input-field"
                        placeholder="e.g. Gold Standard, HMO Plus"
                        required
                    />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 'var(--space-md)' }}>
                    <div className="input-group">
                        <label className="input-label">Deductible ($)</label>
                        <input
                            type="number"
                            name="deductible"
                            value={formData.deductible}
                            onChange={handleChange}
                            className="input-field"
                            min="0"
                            required
                        />
                    </div>
                    <div className="input-group">
                        <label className="input-label">Copay ($)</label>
                        <input
                            type="number"
                            name="copay"
                            value={formData.copay}
                            onChange={handleChange}
                            className="input-field"
                            min="0"
                            required
                        />
                    </div>
                    <div className="input-group">
                        <label className="input-label">Coinsurance (%)</label>
                        <input
                            type="number"
                            name="coinsurance"
                            value={formData.coinsurance}
                            onChange={handleChange}
                            className="input-field"
                            min="0"
                            max="100"
                            required
                        />
                    </div>
                </div>

                <div style={{ marginTop: 'var(--space-lg)', textAlign: 'right' }}>
                    <button type="submit" className="btn btn-primary" style={{ width: '100%', fontSize: '1.125rem' }}>
                        Save & Continue to Symptom Checker →
                    </button>
                </div>
            </form>
        </div>
    );
}
