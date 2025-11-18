_D='file_name'
_C='longitude'
_B='latitude'
_A=None
import math
def haversine_distance(lat1,lon1,lat2,lon2):B=6371000;C=math.radians(lat1);D=math.radians(lat2);E=math.radians(lat2-lat1);F=math.radians(lon2-lon1);A=math.sin(E/2)**2+math.cos(C)*math.cos(D)*math.sin(F/2)**2;G=2*math.atan2(math.sqrt(A),math.sqrt(1-A));return B*G
def find_nearest_image(drawing_point,user_id,api_client):
	D=drawing_point;G,E=api_client.get_tracklog()
	if not G or not E:print(f"[Image Finder] No coordinates found for user {user_id}");return
	C=float('inf');B=_A
	for A in E:
		if not A.get(_B)or not A.get(_C):continue
		F=haversine_distance(D['lat'],D['lng'],A[_B],A[_C])
		if F<C:C=F;B=A.get(_D)
	if B:print(f"[Image Finder] Found nearest image '{B}' at {C:.2f}m distance")
	else:print('[Image Finder] No valid image found')
	return B
def find_nearest_images_batch(drawing_points,user_id,api_client):
	A=drawing_points;J,C=api_client.get_tracklog()
	if not J or not C:print(f"[Image Finder] No coordinates found for user {user_id}");return[_A]*len(A)
	D=[A for A in C if A.get(_B)and A.get(_C)]
	if not D:print('[Image Finder] No valid coordinates found');return[_A]*len(A)
	E=[]
	for F in A:
		G=float('inf');H=_A
		for B in D:
			I=haversine_distance(F['lat'],F['lng'],B[_B],B[_C])
			if I<G:G=I;H=B.get(_D)
		E.append(H)
	return E