"""Test that sample data files work correctly with the RSAI pipeline"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

from rsai.src.data.ingestion import DataIngestion, RepeatSalesProcessor
from rsai.src.data.validation import DataValidator
from rsai.src.main import RSAIPipeline


class TestSampleData:
    """Test using the provided sample data files"""
    
    @pytest.fixture
    def sample_data_paths(self):
        """Get paths to sample data files"""
        base_path = Path(__file__).parent.parent / "data" / "sample"
        
        return {
            'transactions': base_path / "transactions.csv",
            'geographic': base_path / "geographic.csv", 
            'weighting': base_path / "weighting.csv"
        }
    
    def test_sample_data_files_exist(self, sample_data_paths):
        """Test that all sample data files exist"""
        for name, path in sample_data_paths.items():
            assert path.exists(), f"Sample {name} file not found at {path}"
            assert path.is_file(), f"Sample {name} path is not a file: {path}"
    
    def test_load_sample_transaction_data(self, sample_data_paths):
        """Test loading sample transaction data"""
        ingestion = DataIngestion()
        
        # Load the sample transaction data
        df = ingestion.load_transaction_data(str(sample_data_paths['transactions']))
        
        # Check basic structure
        assert len(df) > 0, "Transaction data should not be empty"
        assert 'property_id' in df.columns
        assert 'transaction_date' in df.columns
        assert 'transaction_price' in df.columns
        assert 'census_tract_2010' in df.columns
        assert 'cbsa_id' in df.columns
        
        # Check data types
        assert pd.api.types.is_datetime64_any_dtype(df['transaction_date'])
        assert pd.api.types.is_numeric_dtype(df['transaction_price'])
        
        # Check data quality
        assert df['transaction_price'].min() > 0, "All prices should be positive"
        assert not df['property_id'].isna().any(), "No missing property IDs"
        
        print(f"Loaded {len(df)} transactions from sample data")
        print(f"Date range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
        print(f"Price range: ${df['transaction_price'].min():,.0f} to ${df['transaction_price'].max():,.0f}")
    
    def test_load_sample_geographic_data(self, sample_data_paths):
        """Test loading sample geographic data"""
        ingestion = DataIngestion()
        
        df = ingestion.load_geographic_data(str(sample_data_paths['geographic']))
        
        # Check structure
        assert len(df) > 0, "Geographic data should not be empty"
        assert 'census_tract_2010' in df.columns
        assert 'centroid_lat' in df.columns
        assert 'centroid_lon' in df.columns
        assert 'cbsa_id' in df.columns
        
        # Check coordinate bounds
        assert all(-90 <= lat <= 90 for lat in df['centroid_lat']), "Invalid latitudes"
        assert all(-180 <= lon <= 180 for lon in df['centroid_lon']), "Invalid longitudes"
        
        print(f"Loaded {len(df)} census tracts from sample data")
        print(f"Unique CBSAs: {df['cbsa_id'].nunique()}")
    
    def test_load_sample_weighting_data(self, sample_data_paths):
        """Test loading sample weighting data"""
        ingestion = DataIngestion()
        
        df = ingestion.load_weighting_data(str(sample_data_paths['weighting']))
        
        # Check structure
        assert len(df) > 0, "Weighting data should not be empty"
        assert 'census_tract_2010' in df.columns
        assert 'year' in df.columns
        
        # Check optional fields are present
        expected_fields = [
            'total_housing_units', 'total_housing_value', 'total_upb',
            'college_population', 'non_white_population'
        ]
        for field in expected_fields:
            assert field in df.columns, f"Missing weighting field: {field}"
        
        print(f"Loaded {len(df)} weighting records from sample data")
        print(f"Year range: {df['year'].min()} to {df['year'].max()}")
    
    def test_sample_data_validation(self, sample_data_paths):
        """Test that sample data passes validation"""
        ingestion = DataIngestion()
        validator = DataValidator()
        
        # Load data
        transactions_df = ingestion.load_transaction_data(str(sample_data_paths['transactions']))
        geographic_df = ingestion.load_geographic_data(str(sample_data_paths['geographic']))
        
        # Validate transactions
        trans_issues = validator.validate_transactions(transactions_df)
        assert not trans_issues.get('missing_values', {}), "Sample transaction data has missing values"
        
        # Validate geographic data
        geo_issues = validator.validate_geographic_data(geographic_df)
        assert not geo_issues.get('data_quality', {}), "Sample geographic data has quality issues"
        
        print("Sample data validation passed!")
    
    def test_repeat_sales_processing_with_sample_data(self, sample_data_paths):
        """Test repeat sales processing with sample data"""
        ingestion = DataIngestion()
        processor = RepeatSalesProcessor()
        
        # Load transaction data
        transactions_df = ingestion.load_transaction_data(str(sample_data_paths['transactions']))
        
        # Process repeat sales
        repeat_sales_df = processor.process_repeat_sales(transactions_df)
        
        # Check results
        assert len(repeat_sales_df) > 0, "Should find some repeat sales in sample data"
        
        # Check required columns
        required_columns = [
            'property_id', 'first_sale_date', 'first_sale_price',
            'second_sale_date', 'second_sale_price', 'log_price_relative',
            'annual_growth_rate', 'years_between_sales', 'cumulative_appreciation'
        ]
        
        for col in required_columns:
            assert col in repeat_sales_df.columns, f"Missing column: {col}"
        
        # Check data quality
        assert all(repeat_sales_df['years_between_sales'] > 0), "Invalid time periods"
        assert all(repeat_sales_df['second_sale_date'] > repeat_sales_df['first_sale_date']), "Invalid sale order"
        
        print(f"Found {len(repeat_sales_df)} repeat sales pairs in sample data")
        print(f"Average years between sales: {repeat_sales_df['years_between_sales'].mean():.1f}")
        print(f"Average annual growth rate: {repeat_sales_df['annual_growth_rate'].mean():.1%}")
    
    def test_data_compatibility(self, sample_data_paths):
        """Test that transaction and geographic data are compatible"""
        ingestion = DataIngestion()
        
        # Load both datasets
        transactions_df = ingestion.load_transaction_data(str(sample_data_paths['transactions']))
        geographic_df = ingestion.load_geographic_data(str(sample_data_paths['geographic']))
        
        # Check tract compatibility
        trans_tracts = set(transactions_df['census_tract_2010'].unique())
        geo_tracts = set(geographic_df['census_tract_2010'].unique())
        
        # All transaction tracts should have geographic data
        missing_geo = trans_tracts - geo_tracts
        if missing_geo:
            print(f"Warning: {len(missing_geo)} transaction tracts missing geographic data")
        
        # Check CBSA compatibility
        trans_cbsas = set(transactions_df['cbsa_id'].unique())
        geo_cbsas = set(geographic_df['cbsa_id'].unique())
        
        common_cbsas = trans_cbsas & geo_cbsas
        assert len(common_cbsas) > 0, "No common CBSAs between transaction and geographic data"
        
        print(f"Data compatibility check:")
        print(f"  Transaction tracts: {len(trans_tracts)}")
        print(f"  Geographic tracts: {len(geo_tracts)}")
        print(f"  Common CBSAs: {len(common_cbsas)}")
    
    @pytest.mark.slow
    def test_mini_pipeline_with_sample_data(self, sample_data_paths):
        """Test a mini version of the RSAI pipeline with sample data"""
        # This is a simplified test that doesn't run the full pipeline
        # but tests key components with sample data
        
        ingestion = DataIngestion()
        processor = RepeatSalesProcessor()
        
        # Load data
        transactions_df = ingestion.load_transaction_data(str(sample_data_paths['transactions']))
        geographic_df = ingestion.load_geographic_data(str(sample_data_paths['geographic']))
        
        # Process repeat sales
        repeat_sales_df = processor.process_repeat_sales(transactions_df)
        
        # Basic pipeline validation
        assert len(repeat_sales_df) > 0, "Pipeline should produce repeat sales"
        
        # Check that we can group by year
        repeat_sales_df['sale_year'] = repeat_sales_df['second_sale_date'].dt.year
        yearly_stats = repeat_sales_df.groupby('sale_year').agg({
            'annual_growth_rate': ['count', 'mean', 'std']
        }).round(4)
        
        print("Yearly repeat sales statistics from sample data:")
        print(yearly_stats)
        
        # Should have multiple years of data
        assert len(yearly_stats) > 1, "Should have multiple years of data"


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])