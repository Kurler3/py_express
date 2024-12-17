
import unittest

# Example implementation of the method (to test)
class RouteChecker:
    def _check_route_match(self, route, path):
        # Split both the route and the path by /
        route_split = route.split('/')
        path_split = path.split('/')

        if len(route_split) != len(path_split):
            return False

        for i in range(len(route_split)):
            if route_split[i].startswith(':') and path_split[i] != '':
                continue

            if route_split[i] != path_split[i]:
                return False

        return True

# Unit tests
class TestCheckRouteMatch(unittest.TestCase):
    def setUp(self):
        # Initialize RouteChecker instance for testing
        self.route_checker = RouteChecker()

    def test_exact_match(self):
        # Test for exact match between route and path
        self.assertTrue(self.route_checker._check_route_match('/a/b/c', '/a/b/c'))

    def test_dynamic_match(self):
        # Test where dynamic segments (e.g., :var) match successfully
        self.assertTrue(self.route_checker._check_route_match('/a/:id/c', '/a/123/c'))
        self.assertTrue(self.route_checker._check_route_match('/user/:name', '/user/john'))
    
    def test_mismatch(self):
        # Test cases where route and path don't match
        self.assertFalse(self.route_checker._check_route_match('/a/b/c', '/a/b/d'))
        self.assertFalse(self.route_checker._check_route_match('/a/b/c', '/x/y/z'))

    def test_length_mismatch(self):
        # Test when the route and path have different lengths
        self.assertFalse(self.route_checker._check_route_match('/a/b/c', '/a/b'))
        self.assertFalse(self.route_checker._check_route_match('/a/b', '/a/b/c'))

    def test_empty_route_and_path(self):
        # Test empty route and path (should match)
        self.assertTrue(self.route_checker._check_route_match('', ''))

    def test_one_empty(self):
        # Test one being empty and the other not
        self.assertFalse(self.route_checker._check_route_match('', '/a/b/c'))
        self.assertFalse(self.route_checker._check_route_match('/a/b/c', ''))

    def test_trailing_slashes(self):
        # Test routes and paths with trailing slashes (as edge cases)
        self.assertFalse(self.route_checker._check_route_match('/a/b/c/', '/a/b/c'))
        self.assertTrue(self.route_checker._check_route_match('/a/:var/', '/a/123/'))

if __name__ == '__main__':
    unittest.main()
