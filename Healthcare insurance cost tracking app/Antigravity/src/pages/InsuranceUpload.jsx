import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export default function InsuranceUpload() {
    const navigate = useNavigate();
    const [isDragging, setIsDragging] = useState(false);
    const [isUploading, setIsUploading] = useState(false);

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        // Simulate file drop
        startUpload();
    };

    const startUpload = () => {
        setIsUploading(true);
        // Mock extraction delay
        setTimeout(() => {
            const extractedData = {
                insuranceCompany: 'UnitedHealthcare',
                planName: 'Choice Plus',
                deductible: 2500,
                copay: 35,
                coinsurance: 15,
                age: 42, // Mocked extraction
                gender: 'male',
                state: 'IL'
            };
            navigate('/profile-setup', { state: { extractedData } });
        }, 2000);
    };

    const handleSkip = () => {
        navigate('/profile-setup');
    };

    return (
        <div style={{ maxWidth: '700px', margin: '0 auto', textAlign: 'center' }}>
            <h1 style={{ fontSize: '2.5rem', marginBottom: 'var(--space-md)', color: 'var(--color-primary-dark)' }}>
                Let's Get You Covered
            </h1>
            <p style={{ color: 'var(--color-text-muted)', fontSize: '1.125rem', marginBottom: 'var(--space-xl)' }}>
                Upload your insurance policy document to automatically fill in your details.
            </p>

            <div
                className="card"
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                style={{
                    border: `2px dashed ${isDragging ? 'var(--color-primary)' : 'var(--color-border)'}`,
                    background: isDragging ? 'var(--color-surface-alt)' : 'var(--color-surface)',
                    padding: 'var(--space-xl)',
                    marginBottom: 'var(--space-lg)',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
                }}
            >
                {isUploading ? (
                    <div style={{ padding: 'var(--space-lg)' }}>
                        <div style={{
                            width: '40px',
                            height: '40px',
                            border: '4px solid var(--color-border)',
                            borderTopColor: 'var(--color-primary)',
                            borderRadius: '50%',
                            margin: '0 auto var(--space-md)',
                            animation: 'spin 1s linear infinite'
                        }} />
                        <style>{`@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }`}</style>
                        <h3 style={{ color: 'var(--color-primary)' }}>Analyzing Document...</h3>
                        <p style={{ color: 'var(--color-text-muted)' }}>Extracting coverage details</p>
                    </div>
                ) : (
                    <div onClick={startUpload}>
                        <div style={{ fontSize: '3rem', marginBottom: 'var(--space-sm)' }}>📄</div>
                        <h3 style={{ marginBottom: 'var(--space-xs)' }}>Drop your PDF here</h3>
                        <p style={{ color: 'var(--color-text-muted)', marginBottom: 'var(--space-md)' }}>or click to browse</p>
                        <button className="btn btn-primary">Select Document</button>
                    </div>
                )}
            </div>

            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 'var(--space-md)' }}>
                <div style={{ height: '1px', background: 'var(--color-border)', width: '100px' }} />
                <span style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>OR</span>
                <div style={{ height: '1px', background: 'var(--color-border)', width: '100px' }} />
            </div>

            <button
                onClick={handleSkip}
                className="btn btn-outline"
                style={{ marginTop: 'var(--space-lg)', width: '100%', maxWidth: '300px' }}
            >
                I don't have a document
            </button>
        </div>
    );
}
