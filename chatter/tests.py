from django.test import TestCase

# Create your tests here.

                            # <div class="likes">
                            #     <form action="{% url 'likes' post.pk %}" method="post">
                            #         {% csrf_token %}
                            #         <input type="hidden" name="next" value="{{ request.path }}">
                            #         <button style="background-color: transparent; border:none;box-shadow:none" type="submit"><i class="fas fa-thumbs-up">{{ post.likes.all.count }}</i></button>
                            #     </form>
                            #     <form action="{% url 'dislikes' post.pk %}" method="post">
                            #         {% csrf_token %}
                            #         <input type="hidden" name="next" value="{{ request.path }}">
                            #         <button style="background-color: transparent; border:none;box-shadow:none" type="submit"><i class="fas fa-thumbs-down">{{ post.dislikes.all.count }}</i></button>
                            #     </form>
                            # </div>