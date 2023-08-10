import random
from .models import SecretSantaAssignment, Member

def secret_santa_algorithm(group):
    """
    Executes the Secret Santa algorithm for the given group.

    :param group: The Group object for which to run the Secret Santa algorithm.
    :type group: models.Group
    """

    # Retrieve all members related to the group and include their associated user information.
    members = Member.objects.filter(group=group).select_related('user')

    # Create two lists of members, one for givers and one for receivers, then shuffle the receivers.
    givers = list(members)
    receivers = list(members)
    random.shuffle(receivers)

    # Pair givers with receivers using the zip function.
    assignments = zip(givers, receivers)

    # Remove any previous assignments for the given group.
    SecretSantaAssignment.objects.filter(group=group).delete()

    # Iterate over the giver-receiver pairs, creating new Secret Santa assignments.
    for giver, receiver in assignments:
        # Ensure the giver and receiver are not the same person.
        if giver.user != receiver.user:
            assignment = SecretSantaAssignment(
                group=group,
                giver=giver.user,
                receiver=receiver.user
            )
            assignment.save()
