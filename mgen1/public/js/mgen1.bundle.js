// Import Frappe libraries
import './frappe/public/js/frappe/utils';

// Workspace Charts
frappe.provide('mgen1.workspace.charts');

mgen1.workspace.charts = {
    // Member Distribution Chart
    'توزيع الأعضاء حسب الجهات': function() {
        return {
            type: 'pie',
            data: {
                labels: [],
                datasets: [
                    {
                        name: "الأعضاء",
                        values: []
                    }
                ]
            },
            route_options: {
                doctype: 'عضو'
            },
            async get_data() {
                const data = await frappe.db.get_list('عضو', {
                    fields: ['region', 'count(name) as count'],
                    group_by: 'region'
                });
                
                this.data.labels = data.map(d => d.region);
                this.data.datasets[0].values = data.map(d => d.count);
                return this.data;
            }
        };
    },

    // Income vs Expenses Chart
    'المداخيل والمصاريف': function() {
        return {
            type: 'bar',
            data: {
                labels: [],
                datasets: [
                    {
                        name: "المداخيل",
                        values: []
                    },
                    {
                        name: "المصاريف",
                        values: []
                    }
                ]
            },
            async get_data() {
                const currentYear = frappe.datetime.get_today().split('-')[0];
                const months = Array.from({length: 12}, (_, i) => i + 1);
                
                // Get income data
                const income = await frappe.db.get_list('المداخل', {
                    fields: ['MONTH(date) as month', 'sum(total_amount) as amount'],
                    filters: {
                        date: ['like', `${currentYear}%`],
                        docstatus: 1
                    },
                    group_by: 'MONTH(date)'
                });

                // Get expense data
                const expenses = await frappe.db.get_list('المصارف', {
                    fields: ['MONTH(date) as month', 'sum(total_amount) as amount'],
                    filters: {
                        date: ['like', `${currentYear}%`],
                        docstatus: 1
                    },
                    group_by: 'MONTH(date)'
                });

                // Prepare data
                this.data.labels = months.map(m => frappe.datetime.get_month_name(m));
                this.data.datasets[0].values = months.map(m => {
                    const found = income.find(i => i.month === m);
                    return found ? found.amount : 0;
                });
                this.data.datasets[1].values = months.map(m => {
                    const found = expenses.find(e => e.month === m);
                    return found ? found.amount : 0;
                });

                return this.data;
            }
        };
    }
};
