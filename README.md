# Earthquakes

Lead: epeguero  Emilio Peguero
Designer: cwhite29  
SWE: tmcdile  
Tester: dnichol5  DeAnna Nichols

Prioritized Project Ideas:
1. CPSC Register  
2. CPSC Core Curriculum Recommender  
3. CPSC Degree Works  
4. CPSC Study Buddies  
5. CPSC Electives  
6. CPSC Course Offerings

----------------------------------------------------------------
Data Base Structure:

Database/
│
├── Accounts.txt               (stores all user accounts)
├── Courses.csv                (shows how course files should be formatted)
├── Security_Pins.txt          (pins needed for professor/admin signup)
├── University_Database.csv    (list of all IDs and what type they are)
│
└── courses/                   (folder that holds every course file)
      ├── Comp Sci.txt         (info about one course)
      ├── Math 101.txt         (info about one course)
      └── ...                  (more courses)
