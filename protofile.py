import struct as s


def read_process_binary_file(binary_file_name):
    """
        Reads and processes a binary file according to a specific file structure.

        The binary file is expected to have a header that includes a magic string,
        version byte, and a 4-byte integer indicating the number of records.

        Each record is expected to have a byte indicating the record type, a 4-byte
        Unix timestamp, an 8-byte user ID, and for certain record types namely credit or debit, an 8-byte
        floating point number representing a financial credit or debit amount.

        This function reads the file, interprets the bytes according to this structure,
        and calculates total debit and credit amounts. It also calculates the balance (credits - debits)
        for a given user id

        Args:
            binary_file_name (str): The name of the binary file to be read and processed.

        Returns:
            dict: A dictionary containing 'total credit amount', 'total debit amount',
                  and 'balance', rounded to 2 decimal places.
            'balance' is calculated as 'total credit amount' - 'total debit amount'.
    """
    # define the dictionary for capturing the totals
    dict_output_totals = {
        'total credit amount': 0.0,
        'total debit amount': 0.0,
        'autopays started': 0,
        'autopays ended': 0
    }
    user_id_to_find_credit = 0.0
    user_id_to_find_debit = 0.0
    user_id_to_find_balance = 2456938384156277127
    with open(binary_file_name, 'rb') as f:  # opening the binary file in read mode
        magic_binary = f.read(4)  # read and unpack the magic string as binary string
        magic_string = magic_binary.decode('utf-8')  # Change the binary string to UTF-8 format for string comparisons
        s.unpack('>B', f.read(1))[0]  # unpack the version
        num_records = s.unpack('>I', f.read(4))[0]  # read and unpack the number of records 'I' stands for unsigned int (uint32), 4 bytes
        if magic_string == 'MPS7':  # Validating the magic string to ensure we are parsing the correct file format
            for _ in range(num_records):
                # read and unpack the record type [0] is used to read the first element from a one element tuple from unpack
                record_type = s.unpack('>B', f.read(1))[0]
                # read and unpack the Unix timestamp
                timestamp = s.unpack('>I', f.read(4))[0]
                # read and unpack the user ID
                user_id = s.unpack('>Q', f.read(8))[0]  # 'Q' stands for uint64 8 bytes
                dict_output_totals['total credit amount'] = dict_output_totals['total credit amount']
                # read and unpack the cost and keep track of total credit or total debit if record type is Debit or Credit and if autopay then keep track of startautopay and endautopay
                if record_type == 0x00:  # Debit
                    cost = s.unpack('>d', f.read(8))[0]
                    dict_output_totals['total debit amount'] += cost
                    if user_id == user_id_to_find_balance:  # obtaining the total credit for user id 2456938384156277127
                        user_id_to_find_debit += cost
                elif record_type == 0x01:  # Credit
                    cost = s.unpack('>d', f.read(8))[0]
                    dict_output_totals['total credit amount'] += cost
                    if user_id == user_id_to_find_balance:
                        user_id_to_find_credit += cost  # obtaining the total debit for user id 2456938384156277127
                elif record_type == 0x02:  # autopays started
                    dict_output_totals['autopays started'] += 1
                elif record_type == 0x03:  # autopays ended
                    dict_output_totals['autopays ended'] += 1
    for key, value in dict_output_totals.items():
        if key in ['total debit amount', 'total credit amount']:
            value = round(value, 2)  # rounding to 2 decimal places for credit and debit totals
        print(f'{key}={value}')
    print(f'balance for user id {user_id_to_find_balance}={user_id_to_find_credit - user_id_to_find_debit}')


# Call the function passing the file
read_process_binary_file('txnlog.dat')
