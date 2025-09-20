\# KV Store Project 1 - The Simple Key-Value Store



Student Name: Likitha



EUID: 11682461



---



Project Description



This is a command line application which implements a simple key-value store



The program has three possible commands which can be executed by the user:



```

SET <key> <value>`  

```

This command saves the value under a key. If the key already has a value there, the new value overwrites the previous value. 



```

GET <key>`  

```

This command gets the value for the given key. If the key does not exist, it returns `NULL`.



```

EXIT `

```

This command terminates the application.  



\### Features



\- Append-only persistence: All data is stored by the `SET` command in a logfile `data.db` in the form of a linear sequence.



\- Data with recovery on program restarts: The program replays `data.db` on start-up to restore the in-memory state.  



\- User-defined index for data stored in the computer's memory: The program employs a privately constructed index of \[key, value] pairs instead of using the programmable map/dictionary.



\- The last one to write is given priority: If two values for a key are given, the latest one is stored.



---



\### Instructions to Run the Program



PowerShell has to be opened first, then move to the project folder.



```powershell

cd  C:\\Users\\addal\\OneDrive\\Desktop\\kvstore-project1\\

```

running the command : python kv.py





Enter commands interactively:





SET name Likitha

GET name

GET missing

EXIT

Expected output:



Likitha

NULL






