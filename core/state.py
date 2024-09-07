class State:
    def parseMove(self, move: str):
        """
        converts a human-friendly string representation of a move to a code-friendly representation
        for [isLegal()] and [resolveMove()] to work with
        """
        return None
    
    def isLegal(self, move) -> bool:
        """checks if a move is legal"""
        return bool(move)
    
    def resolveMove(self, move):
        """resolves a move"""
        return None

    pass