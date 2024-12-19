from app.models import User, UserRole, MedicineCategory, Medicine
from app import app, db, dao
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import redirect, request, render_template
import json

admin = Admin(app=app, name='ClinicManagement Admin', template_mode='bootstrap4')


# Base class for admin views
class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


# Logout view
class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/login')


# Stats for medicine usage
class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats_medicine = dao.stats_by_medic(
            kw=request.args.get('kw'),
            from_date=request.args.get('from_date'),
            to_date=request.args.get('to_date')
        )
        return self.render('admin/stats.html', statsMedicine=stats_medicine)


# Stats for revenue
class StatsView1(AuthenticatedView):
    @expose('/')
    def index(self):
        stats_revenue = dao.stats_by_revenue(month=request.args.get('month'))
        return self.render('admin/stats1.html', statsRevenue=stats_revenue)


# Rules management view
class MyRuleView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

    @expose('/', methods=['GET', 'POST'])
    def quy_dinh(self):
        err_msg = ""
        quy_dinh = {"tien_kham": 0, "so_benh_nhan": 0}
        try:
            with open("app/data/quy_dinh.json", "r") as file:
                quy_dinh = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            err_msg = "Không tìm thấy hoặc lỗi đọc file quy định."

        if request.method == "POST":
            tien_kham = request.form.get("tien_kham", "0")
            so_benh_nhan = request.form.get("so_benh_nhan", "0")

            if not tien_kham.isdigit() or not so_benh_nhan.isdigit():
                err_msg = "Vui lòng nhập số hợp lệ cho tiền khám và số bệnh nhân."
            else:
                tien_kham = int(tien_kham)
                so_benh_nhan = int(so_benh_nhan)
                if tien_kham <= 0 or so_benh_nhan <= 0:
                    err_msg = "Số tiền khám hoặc số bệnh nhân phải lớn hơn 0."
                else:
                    quy_dinh["tien_kham"] = tien_kham
                    quy_dinh["so_benh_nhan"] = so_benh_nhan
                    try:
                        with open("data/quy_dinh.json", "w") as file:
                            json.dump(quy_dinh, file)
                    except IOError:
                        err_msg = "Không thể ghi dữ liệu vào file."
                    return self.render("admin/rule.html", quy_dinh=quy_dinh, err_msg=err_msg)

        return self.render('admin/rule.html', quy_dinh=quy_dinh, err_msg=err_msg)


# Admin panel views
admin.add_view(AdminView(User, db.session))
admin.add_view(AdminView(MedicineCategory, db.session))
admin.add_view(AdminView(Medicine, db.session))
admin.add_view(MyRuleView(name="Quy định"))
admin.add_view(StatsView(name='Thống kê - Báo cáo sử dụng thuốc'))
admin.add_view(StatsView1(name='Thống kê - Báo cáo doanh thu'))
admin.add_view(LogoutView(name='Đăng xuất'))
