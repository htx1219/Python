def bowling(balls):
    "Compute the total score for a player's game of bowling."
    init_ball = balls[:]
    score = 0
    for i in range(10):
        if balls[0] == 10:
            score += 10+ balls[1]+balls[2]
            balls = balls[1:]
        elif balls[0]+balls[1] == 10:
            score += 10 + balls[2]
            balls = balls[2:]
        else:
            score += balls[0]+balls[1]
            balls = balls[2:]
    return score


def test_bowling():
    assert   0 == bowling([0] * 20)
    assert  20 == bowling([1] * 20)
    assert  80 == bowling([4] * 20)
    assert 190 == bowling([9,1] * 10 + [9])
    assert 300 == bowling([10] * 12)
    assert 200 == bowling([10, 5,5] * 5 + [10])
    assert  11 == bowling([0,0] * 9 + [10,1,0])
    assert  12 == bowling([0,0] * 8 + [10, 1,0])
    print 'tests pass'

test_bowling()
