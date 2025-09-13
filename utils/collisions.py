
def colliderect(a, b):
    # a later fix
    touching = (
            a.right >= b.left and
            a.left <= b.right and
            a.bottom >= b.top and
            a.top <= b.bottom
    )

    if touching:
        # print(f"[DEBUG] Collision detected! Player={a} | Target={b}")
        return touching


def check_collision(a, b):
    return colliderect(a.rect, b.rect)

