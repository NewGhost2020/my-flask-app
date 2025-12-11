import argparse
import logging
from database import init_db
from parser import run_parser

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Run the promotion parser for Israeli retail sites')
    parser.add_argument(
        '--url',
        type=str,
        default=None,
        help='URL to parse (default: https://bigdabach.co.il)'
    )
    parser.add_argument(
        '--selenium',
        action='store_true',
        help='Use Selenium for parsing (slower but handles dynamic content)'
    )
    parser.add_argument(
        '--store',
        type=str,
        default='BigDaBach',
        help='Store name (default: BigDaBach)'
    )
    parser.add_argument(
        '--init-db',
        action='store_true',
        help='Initialize database before parsing'
    )
    
    args = parser.parse_args()
    
    if args.init_db:
        logger.info("Initializing database...")
        init_db()
        logger.info("Database initialized successfully!")
    
    logger.info(f"Starting parser for {args.store}...")
    
    try:
        stats = run_parser(
            url=args.url,
            use_selenium=args.selenium,
            store_name=args.store
        )
        
        print("\n" + "="*60)
        print("PARSER EXECUTION SUMMARY")
        print("="*60)
        print(f"Store: {args.store}")
        print(f"URL: {args.url or 'https://bigdabach.co.il'}")
        print(f"Method: {'Selenium' if args.selenium else 'Requests'}")
        print("-"*60)
        print(f"Items parsed: {stats['items_parsed']}")
        print(f"Items saved (new): {stats['items_saved']}")
        print(f"Items updated: {stats['items_updated']}")
        print(f"Errors: {stats['errors']}")
        print(f"Duration: {stats['duration']:.2f} seconds")
        print("="*60)
        
        if stats['errors'] > 0:
            logger.warning(f"Parser completed with {stats['errors']} errors")
            return 1
        
        logger.info("Parser completed successfully!")
        return 0
        
    except Exception as e:
        logger.error(f"Parser failed: {str(e)}", exc_info=True)
        return 1


if __name__ == '__main__':
    exit(main())
