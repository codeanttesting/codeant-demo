def analyze_and_process_dataset(data, config=None, verbose=False):
    """
    Complex function that performs comprehensive data analysis and processing.
    Handles validation, transformation, statistical analysis, and report generation.
    
    Args:
        data: List of dictionaries containing transaction records
        config: Optional configuration dictionary
        verbose: Enable detailed logging
    
    Returns:
        Dictionary containing analysis results, processed data, and metadata
    """
    import json
    import hashlib
    from datetime import datetime, timedelta
    from collections import defaultdict, Counter
    import statistics
    
    # Initialize configuration with defaults
    if config is None:
        config = {
            'threshold': 1000,
            'categories': ['electronics', 'clothing', 'food', 'other'],
            'date_format': '%Y-%m-%d',
            'currency': 'USD',
            'tax_rate': 0.08,
            'discount_tiers': [0.05, 0.10, 0.15, 0.20]
        }
    
    # Initialize result containers
    results = {
        'processed_data': [],
        'statistics': {},
        'anomalies': [],
        'summary': {},
        'metadata': {
            'processing_time': None,
            'total_records': 0,
            'valid_records': 0,
            'invalid_records': 0,
            'processing_id': None
        }
    }
    
    start_time = datetime.now()
    errors = []
    category_totals = defaultdict(float)
    monthly_totals = defaultdict(float)
    customer_purchases = defaultdict(list)
    
    # Generate unique processing ID
    process_hash = hashlib.md5(f"{start_time}{len(data)}".encode()).hexdigest()[:8]
    results['metadata']['processing_id'] = process_hash
    
    if verbose:
        print(f"Starting processing with ID: {process_hash}")
        print(f"Total records to process: {len(data)}")
    
    # Data validation and processing loop
    for index, record in enumerate(data):
        try:
            # Validate required fields
            required_fields = ['id', 'amount', 'date', 'customer_id', 'category']
            missing_fields = [field for field in required_fields if field not in record]
            
            if missing_fields:
                errors.append({
                    'index': index,
                    'error': f"Missing fields: {missing_fields}",
                    'record': record
                })
                results['metadata']['invalid_records'] += 1
                continue
            
            # Parse and validate date
            try:
                transaction_date = datetime.strptime(record['date'], config['date_format'])
                month_key = transaction_date.strftime('%Y-%m')
            except ValueError as e:
                errors.append({
                    'index': index,
                    'error': f"Invalid date format: {e}",
                    'record': record
                })
                results['metadata']['invalid_records'] += 1
                continue
            
            # Validate amount
            try:
                amount = float(record['amount'])
                if amount < 0:
                    raise ValueError("Negative amount not allowed")
            except (ValueError, TypeError) as e:
                errors.append({
                    'index': index,
                    'error': f"Invalid amount: {e}",
                    'record': record
                })
                results['metadata']['invalid_records'] += 1
                continue
            
            # Validate category
            category = record.get('category', 'other').lower()
            if category not in config['categories']:
                category = 'other'
            
            # Calculate tax and discounts
            tax_amount = amount * config['tax_rate']
            discount_rate = 0
            
            if amount > 5000:
                discount_rate = config['discount_tiers'][3]
            elif amount > 2000:
                discount_rate = config['discount_tiers'][2]
            elif amount > 1000:
                discount_rate = config['discount_tiers'][1]
            elif amount > 500:
                discount_rate = config['discount_tiers'][0]
            
            discount_amount = amount * discount_rate
            final_amount = amount + tax_amount - discount_amount
            
            # Create processed record
            processed_record = {
                'id': record['id'],
                'customer_id': record['customer_id'],
                'original_amount': amount,
                'tax_amount': round(tax_amount, 2),
                'discount_rate': discount_rate,
                'discount_amount': round(discount_amount, 2),
                'final_amount': round(final_amount, 2),
                'category': category,
                'date': record['date'],
                'month': month_key,
                'processing_timestamp': datetime.now().isoformat(),
                'flags': []
            }
            
            # Check for anomalies
            if amount > config['threshold'] * 10:
                processed_record['flags'].append('high_value')
                results['anomalies'].append({
                    'type': 'high_value_transaction',
                    'record_id': record['id'],
                    'amount': amount,
                    'threshold_exceeded_by': amount - (config['threshold'] * 10)
                })
            
            # Update aggregations
            category_totals[category] += final_amount
            monthly_totals[month_key] += final_amount
            customer_purchases[record['customer_id']].append(final_amount)
            
            results['processed_data'].append(processed_record)
            results['metadata']['valid_records'] += 1
            
        except Exception as e:
            errors.append({
                'index': index,
                'error': f"Unexpected error: {str(e)}",
                'record': record
            })
            results['metadata']['invalid_records'] += 1
    
    # Calculate statistics if we have valid data
    if results['processed_data']:
        all_amounts = [r['final_amount'] for r in results['processed_data']]
        
        results['statistics'] = {
            'total_revenue': round(sum(all_amounts), 2),
            'average_transaction': round(statistics.mean(all_amounts), 2),
            'median_transaction': round(statistics.median(all_amounts), 2),
            'std_deviation': round(statistics.stdev(all_amounts), 2) if len(all_amounts) > 1 else 0,
            'min_transaction': round(min(all_amounts), 2),
            'max_transaction': round(max(all_amounts), 2),
            'total_tax_collected': round(sum(r['tax_amount'] for r in results['processed_data']), 2),
            'total_discounts_given': round(sum(r['discount_amount'] for r in results['processed_data']), 2)
        }
        
        # Category analysis
        results['statistics']['category_breakdown'] = {
            cat: round(total, 2) for cat, total in category_totals.items()
        }
        
        # Monthly trend analysis
        results['statistics']['monthly_trends'] = {
            month: round(total, 2) for month, total in sorted(monthly_totals.items())
        }
        
        # Customer analysis
        customer_totals = {cid: sum(amounts) for cid, amounts in customer_purchases.items()}
        top_customers = sorted(customer_totals.items(), key=lambda x: x[1], reverse=True)[:10]
        results['statistics']['top_customers'] = [
            {'customer_id': cid, 'total_spent': round(total, 2)} 
            for cid, total in top_customers
        ]
        
        # Calculate percentiles
        results['statistics']['percentiles'] = {
            '25th': round(statistics.quantiles(all_amounts, n=4)[0], 2),
            '50th': round(statistics.quantiles(all_amounts, n=4)[1], 2),
            '75th': round(statistics.quantiles(all_amounts, n=4)[2], 2),
            '90th': round(statistics.quantiles(all_amounts, n=10)[8], 2) if len(all_amounts) >= 10 else 0
        }
    
    # Generate summary
    results['summary'] = {
        'success_rate': round((results['metadata']['valid_records'] / len(data)) * 100, 2) if data else 0,
        'processing_date': start_time.strftime('%Y-%m-%d %H:%M:%S'),
        'config_used': config,
        'error_count': len(errors),
        'anomaly_count': len(results['anomalies']),
        'unique_customers': len(customer_purchases),
        'unique_categories': len(category_totals),
        'date_range': {
            'start': min(r['date'] for r in results['processed_data']) if results['processed_data'] else None,
            'end': max(r['date'] for r in results['processed_data']) if results['processed_data'] else None
        }
    }
    
    # Store errors if any
    if errors:
        results['errors'] = errors[:100]  # Limit to first 100 errors
    
    # Calculate processing time
    end_time = datetime.now()
    processing_duration = (end_time - start_time).total_seconds()
    results['metadata']['processing_time'] = f"{processing_duration:.3f} seconds"
    results['metadata']['total_records'] = len(data)
    
    if verbose:
        print(f"Processing completed in {processing_duration:.3f} seconds")
        print(f"Valid records: {results['metadata']['valid_records']}")
        print(f"Invalid records: {results['metadata']['invalid_records']}")
        print(f"Anomalies detected: {len(results['anomalies'])}")
    
    return results