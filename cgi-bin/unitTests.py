import unittest
from structures import *



class TestDbMethods(unittest.TestCase):
    def testAddHumanResourcesCoordinator(self):
        db = {}
        db['volunteers'] = {}
        db['maxVolunteerID'] = 0
        
        self.assertEqual(addHumanResourcesCoordinator(db, "1", "1", "1", 1), True)
        self.assertEqual(addHumanResourcesCoordinator(db, "2", "2", "2", 2), True)
        self.assertEqual(addHumanResourcesCoordinator(db, "3", "3", "3", 3), False)
        
    def testAddMainCoordinator(self):
        db = {}
        db['volunteers'] = {}
        db['maxVolunteerID'] = 0
        
        self.assertEqual(addMainCoordinator(db, "1", "1", "1", 1), True)
        self.assertEqual(addMainCoordinator(db, "2", "2", "2", 2), False)

    def testChangeMainCoordinator(self):
        db = {}
        db['volunteers'] = {}
        db['maxVolunteerID'] = 0
        
        self.assertEqual(changeMainCoordinator(db, "1", "1", "1", 1), 1)
        
        addHumanResourcesCoordinator(db, "2", "2", "2", 2)
        self.assertEqual(changeMainCoordinator(db, "2", "2", "2", 2), 0)

    def testGetId(self):
        db = {}
        db['volunteers'] = {}
        db['maxVolunteerID'] = 0
        
        addMainCoordinator(db, "1", "1", "1", 1)
        addHumanResourcesCoordinator(db, "2", "2", "2", 2)
        addHumanResourcesCoordinator(db, "3", "3", "3", 3)
        
        self.assertEqual(getID(db, "1", "1", "1"), 1)
        self.assertEqual(getID(db, "2", "2", "2"), 2)
        self.assertEqual(getID(db, "3", "3", "3"), 3)
        self.assertEqual(getID(db, "1", "2", "3"), 0)

    def testAddNeed(self):
        db = {}
        db['needs'] = []
        
        addNeed(db, Resource("1","1","1",1,1))
        self.assertEqual(len(db['needs']), 1)
        
        addNeed(db, Resource("1","1","1",1,1))
        self.assertEqual(len(db['needs']), 1)
        
        addNeed(db, Resource("1","2","1",1,1))
        self.assertEqual(len(db['needs']), 2)
        
        addNeed(db, Resource("1","2","1",1,1))
        self.assertEqual(len(db['needs']), 2)
        
        

if __name__ == '__main__':
    unittest.main()
