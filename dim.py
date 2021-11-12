# 2021-10-28 - hieuhihi
import ezdxf

from ancuong import calculator

cakeDim = []
def draw_dim(msp, points, distance=-120, textHeight=100, arrowWidth=50, location=(0, 0), textColor=2, dimcolor=1, dimexo=0, dimexe=0):
    # Reference: https://ezdxf.mozman.at/docs/tutorials/linear_dimension.html
    override = {'dimtxt': textHeight,  # text height
                'dimclrt': textColor,  # text color
                'dimclrd': dimcolor,  # dim color
                'dimclre': dimcolor,  # dim color
                'dimblk': ezdxf.ARROWS.closed_filled,
                'dimasz': arrowWidth,  # arrow width
                'dimtad': 0,
                'dimexo': dimexo,
                'dimexe': dimexe,
                'dimgap': 50,
                'dimtfill': 1  # custom text fill
                }
    global cakeDim
    if int(calculator.distance(points[0], points[1])) < 2:
        return
    elif points[0][0] > points[1][0]:
        dim = msp.add_aligned_dim(p1=(points[1][0], points[1][1]), p2=(points[0][0], points[0][1]),
                                  override=override, distance=-distance)
    else:
        dim = msp.add_aligned_dim(p1=(points[0][0], points[0][1]), p2=(points[1][0], points[1][1]),
                                  override=override, distance=distance)

    dim.set_text(str(int(calculator.distance(points[0], points[1]))))
    if int(calculator.distance(points[0], points[1])) < 300:
        conflict = False
        point = (points[0][0] + points[1][0]) / 2, (points[0][1] + points[1][1]) / 2
        for i in cakeDim:
            if calculator.distance(i, point) < 540:
                conflict = True
        if conflict:
            dim.set_location(location=(location[0], -location[1]), leader=True, relative=True)
        else:
            dim.set_location(location=location, leader=True, relative=True)
        dim.set_text_align(halign='center', valign='above')
        cakeDim.append(point)
    dim.render()