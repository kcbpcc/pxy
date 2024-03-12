def get_kite_broker():
    try:
        sys.stdout = open('output.txt', 'w')
        broker = get_kite(api="bypass", sec_dir=dir_path)  # Assuming dir_path is defined elsewhere
        return broker
    except Exception as e:
        remove_token(dir_path)  # Assuming remove_token function is defined elsewhere
        print(traceback.format_exc())
        logging.error(f"{str(e)} unable to get holdings")
        sys.exit(1)
