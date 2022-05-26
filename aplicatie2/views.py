import random
from math import sqrt, ceil

import numpy as np
import pandas as pd
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect, request
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView
# from gevent.testing import params

from aplicatie2.forms import AddRatingForm
from aplicatie2.models import ResortUserRating
from ski_user_experience.models import AdditionalInformationModel
from webscrapping.models import Resorts


class HomeView(LoginRequiredMixin, ListView):
    model = Resorts
    template_name = 'aplicatie2/home.html'
    context_object_name = 'high_rated_resorts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['visited_resorts'] = AdditionalInformationModel.objects.filter(user=self.request.user)
        context['high_rated_resorts'] = Resorts.objects.filter(rating__gte=4.6)

        img_url = Resorts.objects.values('img')
        image_url_list = [el['img'] for el in img_url]

        resorts = Resorts.objects.all()
        resort_ratings = ResortUserRating.objects.all()
        resort_features = []
        all_resorts_features = []
        resorts_user_ratings = []
        all_resorts_user_ratings = []
        user_input_list = []
        all_user_input_list = []

        # RESORTS DATA FRAME

        for i, resort in enumerate(resorts):
            if resort.img.url == 'None':
                resort_features = [resort.id, resort.name, resort.lowest_point, resort.highest_point,
                                   resort.easy, resort.intermediate, resort.difficult, resort.resort_lift_number,
                                   "/media/media/images/image10.png"]
            else:
                resort_features = [resort.id, resort.name, resort.lowest_point, resort.highest_point,
                                   resort.easy, resort.intermediate, resort.difficult, resort.resort_lift_number,
                                   resort.img.url]

            all_resorts_features += [resort_features]

        resorts_data_frame = pd.DataFrame(all_resorts_features,
                                          columns=['resort_id', 'resort_name', 'resort.lowest_point',
                                                   'resort.highest_point', 'resort.easy',
                                                   'resort.intermediate', 'resort.difficult',
                                                   'lift_number', 'images'])
        print('Resort DataFrame')
        print()
        print(resorts_data_frame)
        print(resorts_data_frame.dtypes)

        # RATING DATA FRAME
        print(resort_ratings)

        for rating in resort_ratings:
            resorts_user_ratings = [rating.user.id, rating.resorts.id, rating.resort_rating]
            all_resorts_user_ratings += [resorts_user_ratings]

        ratings_data_frame = pd.DataFrame(all_resorts_user_ratings, columns=['user_id', 'resort_id', 'rating'])
        ratings_data_frame['user_id'] = ratings_data_frame['user_id'].astype(str).astype(np.int64)
        ratings_data_frame['resort_id'] = ratings_data_frame['resort_id'].astype(str).astype(np.int64)
        ratings_data_frame['rating'] = ratings_data_frame['rating'].astype(str).astype(np.float)

        print(ratings_data_frame)
        print(ratings_data_frame.dtypes)

        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            user_input = ResortUserRating.objects.select_related('resorts').filter(user=user_id)
            if user_input.count() == 0:
                recommender_query, user_input = None, None

            else:
                for item in user_input:
                    user_input_list = [item.resorts.name, item.resort_rating]
                    all_user_input_list += [user_input_list]

            input_resorts = pd.DataFrame(all_user_input_list, columns=['resort_name', 'rating'])
            print("Rated resorts by user Data Frame")
            input_resorts['rating'] = input_resorts['rating'].astype(str).astype(np.int64)
            print(input_resorts.dtypes)

            # FILTERING OUT RESORTS BY NAME

            input_resorts_id = resorts_data_frame[
                resorts_data_frame['resort_name'].isin(input_resorts['resort_name'].tolist())]

            # Then merging it so we can get the resort Id. It's implicitly merging it by the resort name.

            input_Resorts = pd.merge(input_resorts_id, input_resorts)

            print(input_Resorts)

            user_subset = ratings_data_frame[ratings_data_frame['resort_id'].isin(input_Resorts['resort_id'].tolist())]
            user_subset_group = user_subset.groupby(['user_id'])
            user_subset_group = sorted(user_subset_group, key=lambda x: len(x[1]), reverse=True)
            print(user_subset_group[0:])

            user_subset_group = user_subset_group[0:]

            # STORE THE PEARSON CORRELATION IN A DICTIONARY, WHERE THE KEY IS THE user_id THE VALUES IS THE COEFFICIENT
            pearson_correlation_dictionary = {}

            for name, group in user_subset_group:
                # Let's start by sorting the input and current user group so the values aren't mixed up later on
                group = group.sort_values(by='resort_id')
                input_Resorts = input_Resorts.sort_values(by='resort_id')
                # GET THE N FOR THE FORMULA
                n_ratings = len(group)
                # GET THE REVIEW RATINGS FOR THE RESORTS THATH THEY BOTH HAVE IN COMMON
                temp_data_frame = input_Resorts[input_Resorts['resort_id'].isin(group['resort_id'].tolist())]

                temp_rating_list = temp_data_frame['rating'].tolist()
                # STORE THEM IN A TEMP VARIABLE IN A LIST FORMAT
                temp_group_list = group['rating'].tolist()

                # PEARSON CORRELATION BETWEEN USERS

                Sumxx = sum([i ** 2 for i in temp_rating_list]) - pow(sum(temp_rating_list), 2) / float(n_ratings)
                Sumyy = sum([i ** 2 for i in temp_group_list]) - pow(sum(temp_group_list), 2) / float(n_ratings)
                Summxy = sum(i * j for i, j in zip(temp_rating_list, temp_group_list)) - sum(temp_rating_list) * sum(
                    temp_group_list) / float(n_ratings)

                if Sumxx != 0 and Sumyy != 0:
                    pearson_correlation_dictionary[name] = Summxy / sqrt(Sumxx * Sumyy)
                else:
                    pearson_correlation_dictionary[name] = 0

                print(pearson_correlation_dictionary.items())

                pearson_data_frame = pd.DataFrame.from_dict(pearson_correlation_dictionary, orient='index')
                pearson_data_frame.columns = ['similarity_index']
                pearson_data_frame['user_id'] = pearson_data_frame.index
                pearson_data_frame.index = range(len(pearson_data_frame))
                print(pearson_data_frame.head())

                top_users = pearson_data_frame.sort_values(by='similarity_index', ascending=False)[0:]
                print(top_users.head())

                top_users_rating = top_users.merge(ratings_data_frame,
                                                   left_on='user_id',
                                                   right_on='user_id',
                                                   how='inner')
                print(top_users_rating.head())

                # MULTIPLY THE SIMILARITY BY USER RATINGS

                top_users_rating['weighted_rating'] = top_users_rating['similarity_index'] * top_users_rating['rating']

                print(top_users_rating.head())

                # APPLIES A SUM TO THE TOP USERS AFTER GROUPING IT UP BY USER ID

                temp_top_user_rating = top_users_rating.groupby('resort_id').sum()[
                    ['similarity_index', 'weighted_rating']]
                temp_top_user_rating.columns = ['sum_similarity_index', 'sum_weighted_rating']
                temp_top_user_rating.head()

                recommendation_data_frame = pd.DataFrame()

                # POPULATE RECC DF WITH THE WEIGHTED AVERAGE

                recommendation_data_frame['weighted_average_recommendation_score'] = temp_top_user_rating[
                                                                                         'sum_weighted_rating'] / \
                                                                                     temp_top_user_rating[
                                                                                         'sum_similarity_index']
                recommendation_data_frame['resort_id'] = temp_top_user_rating.index
                recommendation_data_frame.head()

                recommendation_data_frame = recommendation_data_frame.sort_values(
                    by='weighted_average_recommendation_score', ascending=False)
                recommender = resorts_data_frame.loc[
                    resorts_data_frame['resort_id'].isin(recommendation_data_frame.head(5)['resort_id'].tolist())]

                print(recommender)
                recommender.rename(columns={'resort.highest_point': 'highest_point'}, inplace=True)
                recommender.rename(columns={'resort.lowest_point': 'lowest_point'}, inplace=True)
                print(recommender)
                context['recommender'] = recommender.to_dict('records')

        return context


class ProfileView(LoginRequiredMixin, ListView):
    model = AdditionalInformationModel
    template_name = 'aplicatie2/profile.html'

    def get_queryset(self):
        return AdditionalInformationModel.objects.filter(user=self.request.user)


class AddRatingView(CreateView):
    model = ResortUserRating
    template_name = 'aplicatie2/resort_rating.html'
    form_class = AddRatingForm

    def get_form_kwargs(self):
        variable_to_send = super(AddRatingView, self).get_form_kwargs()
        variable_to_send.update({'pk': self.request.user.id})

        return variable_to_send

    def get_context_data(self, **kwargs):
        context = super(AddRatingView, self).get_context_data(**kwargs)

        # Already rated resorts
        rated_resorts = ResortUserRating.objects.filter(user=self.request.user)
        rated_resorts_ids = list(rated_resorts.values_list('resorts_id', flat=True))

        # Filter best prices by age
        age = AdditionalInformationModel.objects.values('age', 'user_id')
        age_l = [(el['age'], el['user_id']) for el in age]
        for i in range(len(age_l)):
            if age_l[i][1] == self.request.user.id:
                current_user_age = age_l[i][0]
                if 14 <= int(current_user_age) < 18:
                    context['resorts_prices_filtered_by_age'] = Resorts.objects.filter(rating__gte="3.0").order_by(
                        'youth_ticket').exclude(id__in=rated_resorts_ids)[:4]

                elif int(current_user_age) > 18:
                    context['resorts_prices_filtered_by_age'] = Resorts.objects.filter(rating__gte="3.0").order_by(
                        'adult_ticket').exclude(id__in=rated_resorts_ids)[:4]

        context['dashboard_resorts'] = Resorts.objects.filter(rating__gte="4.0").exclude(id__in=rated_resorts_ids)[:4]
        # filtered_resorts = Resorts.objects.filter(rating__gte = "4.0").exclude(id__in = rated_resorts_ids)[:6]
        # n = len(filtered_resorts)
        # nSlides = n // 4 + ceil((n/4) - (n//4))
        # allRes = [[filtered_resorts, range(1, n), nSlides]]
        # context['dashboard_resorts'] = filtered_resorts

        return context

    def get_success_url(self):
        return reverse('aplicatie2:rating')

#
# class CreateResortView(LoginRequiredMixin, CreateView):
#     model = Resorts
#
#     form_class = ResortsForm
#     template_name = 'aplicatie2/resort_rating.html'
#
#     def get_form_kwargs(self):
#         variable_to_send = super(CreateResortView, self).get_form_kwargs()
#         variable_to_send.update({'pk': None})
#         return variable_to_send
#
#     def get_success_url(self):
#         return reverse('aplicatie2:lista')
#
#
# class UpdateResortView(LoginRequiredMixin, UpdateView):
#     model = Resorts
#     form_class = ResortsForm
#
#     template_name = 'aplicatie2/resort_rating.html'
#
#     def get_form_kwargs(self):
#         variable_to_send = super(UpdateResortView, self).get_form_kwargs()
#         variable_to_send.update({'pk': self.kwargs['pk']})
#         return variable_to_send
#
#     def get_success_url(self):
#         return reverse('aplicatie2:lista')
#


# class UpdateProfile(LoginRequiredMixin, UpdateView):
#     model = UserExtend
#     form_class = NewAccountForm
#     template_name = 'aplicatie2/resort_rating.html'
#
#     def get_queryset(self):
#         return self.model.objects.all()
#
#     def get_success_url(self):
#         return reverse('aplicatie2:lista')
#
#     def get_form_kwargs(self):
#         kwargs = super(UpdateProfile, self).get_form_kwargs()
#         kwargs.update({'current_user': self.request.user.id, 'action': 'update', 'pk': self.kwargs['pk']})
#         return kwargs
#
#
# punctuation = '!@#$%&*'


# class NewAccountView(LoginRequiredMixin, CreateView):
#     model = UserExtend
#     template_name = 'aplicatie1/location_form.html'
#     form_class = NewAccountForm
#
#     def get_form_kwargs(self):
#         kwargs = super(NewAccountView, self).get_form_kwargs()
#         kwargs.update({'current_user': self.request.user.id, 'action': 'create', 'pk': None})
#         return kwargs
#
#     def form_valid(self, form):
#         if form.is_valid():
#             form.save(commit = False)
#         return super(NewAccountView, self).form_valid(form)
#
#     def get_success_url(self):
#         psw = ''.join(random.SystemRandom().choice(string.ascii_uppercase +
#                                                    string.ascii_lowercase +
#                                                    string.digits +
#                                                    punctuation) for _ in range(8))
#
#         if User.objects.filter(id = self.object.id).exists():
#             user_instance = User.objects.get(id = self.object.id)
#             user_instance.set_password(psw)
#             user_instance.username = f"{'.'.join(str(user_instance.first_name).split(' '))}.{'.'.join(user_instance.last_name.split(' '))}"
#             user_instance.save()
#             content_email = f"Username si parola : {user_instance.username} {psw}"
#             msg_html = render_to_string('emails/invite_user.html', {'content_email': content_email})
#             msg = EmailMultiAlternatives(subject = 'New account', body = content_email, from_email = 'contact@test.ro', to = [user_instance.email])
#             msg.attach_alternative(msg_html, 'text/html')
#             msg.send()
#         return reverse('aplicatie2:lista')
#
