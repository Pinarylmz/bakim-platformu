import bcrypt
hash_in_db = b'/57.gWe.Piti6o6r9HRRxu32Sq'
pwd = b'[AdminPlatformLogin]'
print('Match:', bcrypt.checkpw(pwd, hash_in_db))
