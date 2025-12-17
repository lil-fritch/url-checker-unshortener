import time
import concurrent.futures
from src.config import setup_logger
from src.url_processor import load_data_from_pickle, extract_urls, process_single_url

logger = setup_logger()
INPUT_FILE = 'data/messages_to_parse.dat'

def main():
    start_time = time.time()
    logger.info("Starting the application...")

    raw_data = load_data_from_pickle(INPUT_FILE)
    if raw_data is None:
        return

    urls = extract_urls(raw_data)
    if not urls:
        logger.warning("No URLs found. Exiting.")
        return

    url_status_dict = {}
    url_unshorten_dict = {}
    max_threads = 10
    
    logger.info(f"Starting processing of {len(urls)} URLs with {max_threads} threads...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_url = {executor.submit(process_single_url, url): url for url in urls}
        
        for future in concurrent.futures.as_completed(future_to_url):
            orig_url, final_url, status = future.result()
            
            if status is not None:
                url_status_dict[orig_url] = status
                url_unshorten_dict[orig_url] = final_url
                logger.debug(f"Processed: {orig_url} -> {status}")
            else:
                url_status_dict[orig_url] = "Error"
                url_unshorten_dict[orig_url] = "Error"

    end_time = time.time()
    execution_time = end_time - start_time

    logger.success(f"Processing finished in {execution_time:.2f} seconds.")
    logger.info(f"Total processed links: {len(url_status_dict)}")

    print(f"\n--- Statistics for README ---")
    print(f"Execution Time: {execution_time:.2f} seconds")
    print(f"Total URLs processed: {len(url_status_dict)}")

if __name__ == "__main__":
    main()