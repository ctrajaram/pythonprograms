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
            total credit amount: NNNN.NN
            total debit amount: NNNNN.NN
            autopays started N
            autopays ended N
            balance for user 2456938384156277127=N.N
    """
    user_id_to_find_credit = 0.0
    user_id_to_find_debit = 0.0
    user_id_to_find_balance = 2456938384156277127
    debit_total = 0.0
    credit_total = 0.0
    autopay_started = 0
    autopay_ended = 0
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
                # read and unpack the cost and keep track of total credit or total debit if record type is Debit or Credit and if autopay then keep track of startautopay and endautopay
                if record_type == 0x00:  # Debit
                    cost = s.unpack('>d', f.read(8))[0]
                    debit_total += cost
                    if user_id == user_id_to_find_balance:  # obtaining the total credit for user id 2456938384156277127
                        user_id_to_find_debit += cost
                elif record_type == 0x01:  # Credit
                    cost = s.unpack('>d', f.read(8))[0]
                    credit_total += cost
                    if user_id == user_id_to_find_balance:
                        user_id_to_find_credit += cost  # obtaining the total debit for user id 2456938384156277127
                elif record_type == 0x02:  # autopays started
                    autopay_started += 1
                elif record_type == 0x03:  # autopays ended
                    autopay_ended += 1
    print(f"total credit amount: {credit_total:.2f}")
    print(f"total debit amount: {debit_total:.2f}")
    print(f'autopays started {autopay_started}')
    print(f'autopays ended {autopay_ended}')
    print(f'balance for user {user_id_to_find_balance}={user_id_to_find_credit - user_id_to_find_debit}')


# Call the function passing the file
read_process_binary_file('txnlog.dat')
