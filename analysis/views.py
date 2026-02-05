# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Site
# from .serializers import SiteSerializer
# from .calculator import calculate_score

# class SiteAnalysisView(APIView):
#     def get(self, request):
#         sites = Site.objects.all()
#         serializer = SiteSerializer(sites, many=True)
        
#         weights = {
#             'solar': 0.35, 'area': 0.25, 'grid': 0.20, 
#             'slope': 0.15, 'infrastructure': 0.05
#         }
        
#         results = []
#         for site_data in serializer.data:
#             site = Site.objects.get(id=site_data['id'])
#             score_data = calculate_score(site, weights)
#             results.append({**site_data, **score_data})
            
#         return Response(results)

#     def post(self, request):
#         weights = request.data.get('weights', {
#             'solar': 0.35, 'area': 0.25, 'grid': 0.20, 
#             'slope': 0.15, 'infrastructure': 0.05
#         })
#         sites = Site.objects.all()
#         serializer = SiteSerializer(sites, many=True)
        
#         results = []
#         for site_data in serializer.data:
#             site = Site.objects.get(id=site_data['id'])
#             score_data = calculate_score(site, weights)
#             results.append({**site_data, **score_data})
            
#         return Response(results)



from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg, Max, Min, Count
from .models import Site
from .serializers import SiteSerializer
from .calculator import calculate_score

class SiteAnalysisView(APIView):
    def get(self, request, pk=None):
        # Handle GET /api/sites/{id}
        if pk:
            try:
                site = Site.objects.get(pk=pk)
                serializer = SiteSerializer(site)
                # Use default weights for detail view
                weights = {
                    'solar': 0.35, 'area': 0.25, 'grid': 0.20, 
                    'slope': 0.15, 'infrastructure': 0.05
                }
                score_data = calculate_score(site, weights)
                return Response({**serializer.data, **score_data})
            except Site.DoesNotExist:
                return Response({'error': 'Site not found'}, status=404)

        # Handle GET /api/sites/ (List all)
        sites = Site.objects.all()
        serializer = SiteSerializer(sites, many=True)
        
        weights = {
            'solar': 0.35, 'area': 0.25, 'grid': 0.20, 
            'slope': 0.15, 'infrastructure': 0.05
        }
        
        results = []
        for site_data in serializer.data:
            site = Site.objects.get(id=site_data['id'])
            score_data = calculate_score(site, weights)
            results.append({**site_data, **score_data})
            
        return Response(results)

    def post(self, request):
        weights = request.data.get('weights', {
            'solar': 0.35, 'area': 0.25, 'grid': 0.20, 
            'slope': 0.15, 'infrastructure': 0.05
        })
        sites = Site.objects.all()
        serializer = SiteSerializer(sites, many=True)
        
        results = []
        for site_data in serializer.data:
            site = Site.objects.get(id=site_data['id'])
            score_data = calculate_score(site, weights)
            results.append({**site_data, **score_data})
            
        return Response(results)

class StatisticsView(APIView):
    def get(self, request):
        stats = Site.objects.aggregate(
            total_sites=Count('id'),
            avg_area=Avg('area_sqm'),
            avg_irradiance=Avg('solar_irradiance_kwh'),
            max_irradiance=Max('solar_irradiance_kwh'),
            min_grid_dist=Min('grid_distance_km')
        )
        return Response(stats)